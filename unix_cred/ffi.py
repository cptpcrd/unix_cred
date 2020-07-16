# pylint: disable=invalid-name
import ctypes
import ctypes.util

libc_path = ctypes.util.find_library("c")
assert libc_path is not None
libc = ctypes.CDLL(libc_path, use_errno=True)

pid_t = ctypes.c_int
uid_t = ctypes.c_uint32
gid_t = ctypes.c_uint32
