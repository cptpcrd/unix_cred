import contextlib
import ctypes
import dataclasses
import errno
import socket
from typing import Iterator, List, Tuple, Union

from . import ffi, util

libc = ffi.load_libc()

libc.getpeerucred.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))
libc.getpeerucred.restype = ctypes.c_int

libc.ucred_free.argtypes = (ctypes.c_void_p,)
libc.ucred_free.restype = None

libc.ucred_getpid.argtypes = (ctypes.c_void_p,)
libc.ucred_getpid.restype = ffi.pid_t

libc.ucred_getruid.argtypes = (ctypes.c_void_p,)
libc.ucred_getruid.restype = ffi.uid_t
libc.ucred_geteuid.argtypes = (ctypes.c_void_p,)
libc.ucred_geteuid.restype = ffi.uid_t
libc.ucred_getsuid.argtypes = (ctypes.c_void_p,)
libc.ucred_getsuid.restype = ffi.uid_t

libc.ucred_getrgid.argtypes = (ctypes.c_void_p,)
libc.ucred_getrgid.restype = ffi.gid_t
libc.ucred_getegid.argtypes = (ctypes.c_void_p,)
libc.ucred_getegid.restype = ffi.gid_t
libc.ucred_getsgid.argtypes = (ctypes.c_void_p,)
libc.ucred_getsgid.restype = ffi.gid_t

libc.ucred_getgroups.argtypes = (
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.POINTER(ffi.gid_t)),  # pytype: disable=invalid-typevar
)
libc.ucred_getgroups.restype = ctypes.c_int


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


@contextlib.contextmanager
def _getpeerucred_raw(sock: Union[socket.socket, int]) -> Iterator[ctypes.c_void_p]:
    if not isinstance(sock, int):
        sock = sock.fileno()

    raw_ucred = ctypes.c_void_p(None)

    if libc.getpeerucred(sock, ctypes.pointer(raw_ucred)) < 0:
        raise util.build_oserror(ctypes.get_errno())

    if not raw_ucred.value:
        raise util.build_oserror(errno.EINVAL)

    try:
        yield raw_ucred
    finally:
        libc.ucred_free(raw_ucred)


def getpeerucred(sock: Union[socket.socket, int]) -> Ucred:
    with _getpeerucred_raw(sock) as raw_ucred:
        groups_ptr = ctypes.POINTER(ffi.gid_t)()  # pytype: disable=not-callable
        ngroups = libc.ucred_getgroups(raw_ucred, ctypes.pointer(groups_ptr))
        if ngroups < 0:
            raise util.build_oserror(errno.EINVAL)

        groups = [groups_ptr[i].value for i in range(ngroups)]

        return Ucred(
            pid=libc.ucred_getpid(raw_ucred),
            ruid=libc.ucred_getruid(raw_ucred),
            euid=libc.ucred_geteuid(raw_ucred),
            suid=libc.ucred_getsuid(raw_ucred),
            rgid=libc.ucred_getrgid(raw_ucred),
            egid=libc.ucred_getegid(raw_ucred),
            sgid=libc.ucred_getsgid(raw_ucred),
            groups=groups,
        )


def _get_peer_uid_gid(sock: Union[socket.socket, int]) -> Tuple[int, int]:
    with _getpeerucred_raw(sock) as raw_ucred:
        return libc.ucred_geteuid(raw_ucred), libc.ucred_getegid(raw_ucred)


def _get_peer_pid_uid_gid(sock: Union[socket.socket, int]) -> Tuple[int, int, int]:
    with _getpeerucred_raw(sock) as raw_ucred:
        return (
            libc.ucred_getpid(raw_ucred),
            libc.ucred_geteuid(raw_ucred),
            libc.ucred_getegid(raw_ucred),
        )
