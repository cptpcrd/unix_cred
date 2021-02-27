import dataclasses
import errno
import socket
import struct
import sys
from typing import Union

from . import constants, util

if sys.platform.startswith("netbsd"):
    _SO_PEERCRED = constants.LOCAL_PEEREID
    _LEVEL = 0
else:
    _SO_PEERCRED = socket.SO_PEERCRED  # pylint: disable=no-member
    _LEVEL = socket.SOL_SOCKET


_OPENBSD = sys.platform.startswith("openbsd")

_ucred = struct.Struct("=IIi" if _OPENBSD else "=iII")

assert _ucred.size == 12


@dataclasses.dataclass
class Ucred:
    pid: int
    uid: int
    gid: int


def get_ucred(sock: Union[socket.socket, int]) -> Ucred:
    with util.with_socket_or_fd(sock) as sock_obj:
        buf = sock_obj.getsockopt(_LEVEL, _SO_PEERCRED, _ucred.size)

    if _OPENBSD:
        uid, gid, pid = _ucred.unpack(buf)
    else:
        pid, uid, gid = _ucred.unpack(buf)

    return Ucred(pid=pid, uid=uid, gid=gid)
