from hamcrest import *
from pysyscall_intercept import SysCallInterceptor, SYS_WRITE, SYS_OPEN


def test_intercept__no_return():
    class Handler(object):
        def __init__(self):
            self.count = 0

        def on_syscall(self):
            self.count += 1

    handler = Handler()
    with SysCallInterceptor(SYS_WRITE, handler.on_syscall):
        with open('/dev/null', 'w') as f:
            f.write('test')

    assert_that(handler.count, is_(1))


def test_intercept__bool_return():
    class Handler(object):
        def __init__(self):
            self.count = 0

        def on_syscall(self):
            self.count += 1
            return False

    handler = Handler()
    with SysCallInterceptor(SYS_WRITE, handler.on_syscall):
        with open('/dev/null', 'w') as f:
            f.write('test')

    assert_that(handler.count, is_(1))


def test_multiple_interceptors__same_syscall():
    with SysCallInterceptor(SYS_WRITE, lambda: _):
        interceptor2 = SysCallInterceptor(SYS_WRITE, lambda: _)
        assert_that(calling(interceptor2.__enter__), raises(RuntimeError))


def test_multiple_interceptors__different_syscalls():
    with SysCallInterceptor(SYS_WRITE, lambda: _):
        with SysCallInterceptor(SYS_OPEN, lambda: _):
            pass


def test_resuse_interceptor():
    class Handler(object):
        def __init__(self):
            self.count = 0

        def on_syscall(self):
            self.count += 1
            return False

    handler = Handler()
    with SysCallInterceptor(SYS_WRITE, handler.on_syscall):
        with open('/dev/null', 'w') as f:
            f.write('test')

    with open('/dev/null', 'w') as f:
        f.write('test')

    with SysCallInterceptor(SYS_WRITE, handler.on_syscall):
        with open('/dev/null', 'w') as f:
            f.write('test')

    assert_that(handler.count, is_(2))



