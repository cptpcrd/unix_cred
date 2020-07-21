# pylint: disable=invalid-name
import ctypes
import ctypes.util

_libc = None


def load_libc() -> ctypes.CDLL:
    global _libc  # pylint: disable=global-statement

    if _libc is None:
        libc_path = ctypes.util.find_library("c")
        if libc_path is None:
            raise RuntimeError("Could not find libc; is your system statically linked?")

        _libc = ctypes.CDLL(libc_path, use_errno=True)

    return _libc


pid_t = ctypes.c_int
uid_t = ctypes.c_uint32
gid_t = ctypes.c_uint32
