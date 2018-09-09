from hamcrest import *
from pysyscall_intercept import SysCallInterceptor


SYS_READ = 0
SYS_WRITE = 1


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

