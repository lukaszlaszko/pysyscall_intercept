#pragma once

#include <pybind11/pybind11.h>

#include <functional>
#include <memory>
#include <syscall.h>


class syscall_interceptor
{
public:
    template <typename T>
    struct identity
    {
        using type = T;
    };

    using callback_type = std::function<bool(
            long& arg0,
            long& arg1,
            long& arg2,
            long& arg3,
            long& arg4,
            long& arg5,
            long& result)>;

    syscall_interceptor(long syscall_number, callback_type&& callback);

    template <typename... args_types>
    syscall_interceptor(
            long syscall_number,
            typename identity<std::function<bool(long& result, args_types...)>>::type&& callback);

    ~syscall_interceptor();

private:
    template <typename function_type, typename tuple_type, std::size_t... Is>
    static bool invoke(function_type&& function, long& result, tuple_type args, std::index_sequence<Is...>);

    long syscall_number_{0l};
    callback_type callback_;

};

class syscall_interceptor_context
{
public:
    syscall_interceptor_context(long syscall_number, pybind11::function callback);

    syscall_interceptor_context& __enter__();

    void __exit__(
            pybind11::object exc_type,
            pybind11::object exc_value,
            pybind11::object traceback);

private:
    long syscall_number_;
    pybind11::function callback_;

    std::unique_ptr<syscall_interceptor> interceptor_;

};

#include "_interceptor.ipp"
