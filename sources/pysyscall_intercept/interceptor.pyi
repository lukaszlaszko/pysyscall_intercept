from typing import Callable, NoReturn


class SysCallInterceptor:
    def __init__(self,
                 syscall_number: int,
                 callback: Callable[[list], bool]) -> NoReturn: ...

    def __enter__(self) -> NoReturn: ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> NoReturn: ...