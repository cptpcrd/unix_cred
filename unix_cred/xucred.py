import ctypes
import ctypes.util
import dataclasses
import errno
import socket
import sys
from typing import List, Optional, Union

from . import constants, ffi, util

if sys.platform.startswith("freebsd"):

    class _XcuredCr(ctypes.Union):  # pylint: disable=too-few-public-methods
        _fields_ = [
            ("cr_pid", ffi.pid_t),
            ("_cr_unused1", ctypes.c_void_p),
        ]


class _Xucred(ctypes.Structure):  # pylint: disable=too-few-public-methods
    if sys.platform.startswith("freebsd"):
        _anonymous_ = ("_cr",)

        _fields_ = [
            ("cr_version", ctypes.c_uint),
            ("cr_uid", ffi.uid_t),
            ("cr_ngroups", ctypes.c_short),
            ("cr_groups", ffi.gid_t * constants.XU_NGROUPS),
            ("_cr", _XcuredCr),
        ]
    elif sys.platform.startswith("dragonfly"):
        _fields_ = [
            ("cr_version", ctypes.c_uint),
            ("cr_uid", ffi.uid_t),
            ("cr_ngroups", ctypes.c_short),
            ("cr_groups", ffi.gid_t * constants.XU_NGROUPS),
            ("_cr_unused1", ctypes.c_void_p),
        ]
    else:
        _fields_ = [
            ("cr_version", ctypes.c_uint),
            ("cr_uid", ffi.uid_t),
            ("cr_ngroups", ctypes.c_short),
            ("cr_groups", ffi.gid_t * constants.XU_NGROUPS),
        ]

    def convert(self) -> "Xucred":
        if (
            self.cr_version != constants.XUCRED_VERSION
            or self.cr_ngroups < 1
            or self.cr_ngroups > constants.XU_NGROUPS
        ):
            raise util.build_oserror(errno.EINVAL)

        groups = list(self.cr_groups[: self.cr_ngroups])

        return Xucred(
            uid=self.cr_uid, gid=groups[0], groups=groups, pid=(getattr(self, "cr_pid", 0) or None)
        )


@dataclasses.dataclass
class Xucred:
    uid: int
    gid: int

    groups: List[int]

    pid: Optional[int]


def get_xucred(sock: Union[socket.socket, int]) -> Xucred:
    with util.with_socket_or_fd(sock) as sock_obj:
        buf = sock_obj.getsockopt(
            0,
            socket.LOCAL_PEERCRED,  # pylint: disable=no-member
            ctypes.sizeof(_Xucred),
        )

    return _Xucred.from_buffer_copy(buf).convert()
