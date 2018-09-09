#pragma once

#include <functional>
#include <memory>
#include <tuple>
#include <utility>


template <typename... args_types>
inline syscall_interceptor::syscall_interceptor(
        long syscall_number,
        typename identity<std::function<bool(long& result, args_types...)>>::type&& callback)
        :
        syscall_interceptor(
                syscall_number,
                [callback = std::move(callback)](
                        long& inner_result, long& arg0, long& arg1, long& arg2, long& arg3, long& arg4, long& arg5)
                {
                    auto args = std::make_tuple(&arg0, &arg1, &arg2, &arg3, &arg4, &arg5);
                    return invoke(callback, inner_result, args, std::index_sequence_for<args_types...>{});
                })
{

}

template <typename function_type, typename tuple_type, std::size_t... Is>
inline bool syscall_interceptor::invoke(function_type&& function, long& result, tuple_type args, std::index_sequence<Is...>)
{
    return function(result, std::get<Is>(args)...);
}