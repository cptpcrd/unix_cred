import ctypes
import dataclasses
import errno
import socket
from typing import List, Union

from . import ffi, util

ffi.libc.getpeerucred.argtypes = (ctypes.c_int, ctypes.c_void_p)
ffi.libc.getpeerucred.restype = ctypes.c_int

ffi.libc.ucred_free.argtypes = (ctypes.c_void_p,)
ffi.libc.ucred_free.restype = None

ffi.libc.ucred_getpid.argtypes = (ctypes.c_void_p,)
ffi.libc.ucred_getpid.restype = ffi.pid_t

ffi.libc.ucred_getruid.argtypes = (ctypes.c_void_p,)
ffi.libc.ucred_getruid.restype = ffi.uid_t
ffi.libc.ucred_geteuid.argtypes = (ctypes.c_void_p,)
ffi.libc.ucred_geteuid.restype = ffi.uid_t
ffi.libc.ucred_getsuid.argtypes = (ctypes.c_void_p,)
ffi.libc.ucred_getsuid.restype = ffi.uid_t

ffi.libc.ucred_getrgid.argtypes = (ctypes.c_void_p,)
ffi.libc.ucred_getrgid.restype = ffi.gid_t
ffi.libc.ucred_getegid.argtypes = (ctypes.c_void_p,)
ffi.libc.ucred_getegid.restype = ffi.gid_t
ffi.libc.ucred_getsgid.argtypes = (ctypes.c_void_p,)
ffi.libc.ucred_getsgid.restype = ffi.gid_t

ffi.libc.ucred_getgroups.argtypes = (
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.POINTER(ffi.gid_t)),  # pytype: disable=invalid-typevar
)
ffi.libc.ucred_getgroups.restype = ctypes.c_int


@dataclasses.dataclass
class Ucred:  # pylint: disable=too-many-instance-attributes
    pid: int

    ruid: int
    euid: int
    suid: int

    rgid: int
    egid: int
    sgid: int

    groups: List[int]


def getpeerucred(sock: Union[socket.socket, int]) -> Ucred:
    if not isinstance(sock, int):
        sock = sock.fileno()

    raw_ucred = ctypes.c_void_p(None)

    if ffi.libc.getpeerucred(sock, ctypes.pointer(raw_ucred)) < 0:
        raise util.build_oserror(ctypes.get_errno())

    if not raw_ucred.value:
        raise util.build_oserror(errno.EINVAL)

    try:
        groups_ptr = ctypes.POINTER(ffi.gid_t)()  # pytype: disable=not-callable
        ngroups = ffi.libc.ucred_getgroups(raw_ucred, ctypes.pointer(groups_ptr))
        if ngroups < 0:
            raise util.build_oserror(errno.EINVAL)

        groups = [groups_ptr[i].value for i in range(ngroups)]

        ucred = Ucred(
            pid=ffi.libc.ucred_getpid(raw_ucred),
            ruid=ffi.libc.ucred_getruid(raw_ucred),
            euid=ffi.libc.ucred_geteuid(raw_ucred),
            suid=ffi.libc.ucred_getsuid(raw_ucred),
            rgid=ffi.libc.ucred_getrgid(raw_ucred),
            egid=ffi.libc.ucred_getegid(raw_ucred),
            sgid=ffi.libc.ucred_getsgid(raw_ucred),
            groups=groups,
        )
    finally:
        ffi.libc.ucred_free(raw_ucred)

    return ucred
