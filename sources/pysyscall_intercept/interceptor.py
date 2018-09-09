from contextlib import contextmanager
from signal import getsignal, signal, SIGTRAP


@contextmanager
def block_signals(signals):
    def empty_handler(signo, frame):
        pass

    handler = getsignal(SIGTRAP)
    signal(SIGTRAP, empty_handler)
    try:
        yield
    finally:
        signal(SIGTRAP, handler)


with block_signals({SIGTRAP}):
    from _interceptor import *
