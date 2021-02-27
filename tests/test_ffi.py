import ctypes
import os

import unix_cred.ffi


def test_load_libc() -> None:
    libc = unix_cred.ffi.load_libc()
    assert libc is not None

    # Returns the same library
    assert libc is unix_cred.ffi.load_libc()

    libc.nice.argtypes = (ctypes.c_int,)
    libc.nice.restype = ctypes.c_int
    assert libc.nice(0) == os.nice(0)
