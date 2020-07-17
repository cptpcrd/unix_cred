import ctypes
import ctypes.util
import dataclasses
import socket
import sys
from typing import Union

from . import constants, ffi, util

if sys.platform.startswith("netbsd"):
    _SO_PEERCRED = constants.LOCAL_PEEREID
else:
    _SO_PEERCRED = socket.SO_PEERCRED  # pylint: disable=no-member


class _Ucred(ctypes.Structure):  # pylint: disable=too-few-public-methods
    if sys.platform.startswith("openbsd"):
        _fields_ = [
            ("uid", ffi.uid_t),
            ("gid", ffi.gid_t),
            ("pid", ffi.pid_t),
        ]
    else:
        _fields_ = [
            ("pid", ffi.pid_t),
            ("uid", ffi.uid_t),
            ("gid", ffi.gid_t),
        ]

    def convert(self) -> "Ucred":
        return Ucred(pid=self.pid, uid=self.uid, gid=self.gid)


@dataclasses.dataclass
class Ucred:
    pid: int
    uid: int
    gid: int


def get_ucred(sock: Union[socket.socket, int]) -> Ucred:
    with util.with_socket_or_fd(sock) as sock_obj:
        buf = sock_obj.getsockopt(socket.SOL_SOCKET, _SO_PEERCRED, ctypes.sizeof(_Ucred))

    return _Ucred.from_buffer_copy(buf).convert()
