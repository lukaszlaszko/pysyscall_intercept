#include "_interceptor.hpp"

#include <libsyscall_intercept_hook_point.h>
#include <pybind11/pybind11.h>

#include <cerrno>
#include <cstdbool>
#include <cstdlib>
#include <memory>
#include <stdexcept>
#include <unordered_map>

#include <syscall.h>

using namespace std;
namespace py = pybind11;


size_t guards_count = 0ul;
unordered_map<long, syscall_interceptor::callback_type*> guards;

static int hook(long syscall_number,
                long arg0,
                long arg1,
                long arg2,
                long arg3,
                long arg4,
                long arg5,
                long *result)
{
    (void) arg2;
    (void) arg3;
    (void) arg4;
    (void) arg5;

    if (guards_count == 0)
        return 1;

    auto search_result = guards.find(syscall_number);
    if (search_result == guards.end())
        return 1;

    auto& callback = *search_result->second;
    if (!callback)
        return 1;

    if (callback(*result, arg0, arg1, arg2, arg3, arg4, arg5))
    {
        syscall_no_intercept(syscall_number, arg0, arg1, arg2, arg3, arg4, arg5);
        return 0;
    }
    else
        return 1;
}

syscall_interceptor::syscall_interceptor(long syscall_number, callback_type&& callback)
    :
        callback_(move(callback))
{
    if (guards.count(syscall_number) > 0)
        throw runtime_error("syscall_number already registered!");

    guards[syscall_number] = &callback_;
    syscall_number_ = syscall_number;

    guards_count++;
}

syscall_interceptor::~syscall_interceptor()
{
    if (syscall_number_ > 0)
    {
        guards.erase(syscall_number_);
        guards_count--;
    }
}

syscall_interceptor_context::syscall_interceptor_context(
        long syscall_number,
        py::function callback)
    :
        syscall_number_(syscall_number),
        callback_(callback)
{

}

syscall_interceptor_context& syscall_interceptor_context::__enter__()
{
    interceptor_.reset(new syscall_interceptor(syscall_number_, [this](auto& result)
    {
        py::gil_scoped_acquire gil_acquire;

        auto callback_result = callback_();
        if (callback_result.is_none())
            return false;

        if (py::isinstance<bool>(callback_result))
            return callback_result.cast<bool>();
        else if (py::isinstance<long>(callback_result))
        {
            result = callback_result.cast<long>();
            return true;
        }
        else
            return false;
    }));
    return *this;
}

void syscall_interceptor_context::__exit__(
        py::object exc_type,
        py::object exc_value,
        py::object traceback)
{
    interceptor_.reset();
}

PYBIND11_MODULE(_interceptor, m)
{
    intercept_hook_point = &hook;

    py::class_<syscall_interceptor_context>(m, "SysCallInterceptor")
            .def(py::init<long, py::function>(),
                    py::arg("syscall_number"),
                    py::arg("callback"))
            .def("__enter__", &syscall_interceptor_context::__enter__)
            .def("__exit__", &syscall_interceptor_context::__exit__);

}