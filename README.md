[![CircleCI](https://circleci.com/gh/lukaszlaszko/pysyscall_intercept.svg?style=svg)](https://circleci.com/gh/lukaszlaszko/pysyscall_intercept)
[![PyPI version](https://badge.fury.io/py/pysyscall_intercept.svg)](https://badge.fury.io/py/pysyscall_intercept)

## Overview

Python bindings for [syscall_interceptor](https://github.com/pmem/syscall_intercept). 

## Usage

In order to intercept a system call on Linux:
```python
from pysyscall_intercept import SysCallInterceptor, SYS_WRITE

[...]

def on_syscall():
    return False

with SysCallInterceptor(SYS_WRITE, on_syscall):
    with open('/dev/null', 'w') as f:
        f.write('test')
```

Within a scope of instantiated resource manager given callback will be invoked before selected system call. 
Depending on return type of the callback:
- if callback doesn't return anything or `None`, no action will be taken and the system call will be invoked.
- if callback returns a `bool` value:
    - `True`, system call will be suppressed.
    - `False`, system call will be executed after the callback.
- if callback returns an `int` value, system call will be suppressed and given value will simulate 
return value of the system call. 

## Installation

From PyPI:

```
$ pip install pysyscall_intercept
```

Notice that this will only succeed on Linux with `CMake` in version at least 3.7, `pkg-config` and `libcapstone-dev`. You can install those
with:

```
$ sudo apt-get install pkg-config libcapstone-dev (on Debian, Ubuntu)
```   

## Limitations

Currently only CPython on Linux is supported. 