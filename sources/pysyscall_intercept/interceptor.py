from contextlib import contextmanager
from signal import getsignal, signal, SIGTRAP


@contextmanager
def block_sigtrap():
    def empty_handler(signo, frame):
        pass

    handler = getsignal(SIGTRAP)
    signal(SIGTRAP, empty_handler)
    try:
        yield
    finally:
        signal(SIGTRAP, handler)


with block_sigtrap():
    from _interceptor import *





