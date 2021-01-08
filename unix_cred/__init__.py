import socket
import sys
from typing import Optional, Tuple, Union

__version__ = "0.2.1"

__all__ = ["get_peer_uid_gid"]

if sys.platform.startswith(("linux", "openbsd", "netbsd")):
    from . import ucred  # noqa: F401

    __all__.append("ucred")

    def get_peer_uid_gid(sock: Union[socket.socket, int]) -> Tuple[int, int]:
        cred = ucred.get_ucred(sock)
        return cred.uid, cred.gid


elif sys.platform.startswith(("freebsd", "dragonfly", "darwin")):
    from . import xucred  # noqa: F401

    __all__.append("xucred")

    def get_peer_uid_gid(sock: Union[socket.socket, int]) -> Tuple[int, int]:
        cred = xucred.get_xucred(sock)
        return cred.uid, cred.gid


elif sys.platform.startswith(("solaris", "illumos")):
    from . import peerucred  # noqa: F401

    __all__.append("peerucred")

    def get_peer_uid_gid(sock: Union[socket.socket, int]) -> Tuple[int, int]:
        return peerucred._get_peer_uid_gid(sock)  # pylint: disable=protected-access


else:
    raise ValueError("Unsupported platform")


if sys.platform.startswith(("linux", "openbsd", "netbsd")):

    def get_peer_pid_uid_gid(sock: Union[socket.socket, int]) -> Tuple[Optional[int], int, int]:
        cred = ucred.get_ucred(sock)
        return cred.pid, cred.uid, cred.gid

    __all__.append("get_peer_pid_uid_gid")

elif sys.platform.startswith("freebsd"):

    def get_peer_pid_uid_gid(sock: Union[socket.socket, int]) -> Tuple[Optional[int], int, int]:
        cred = xucred.get_xucred(sock)
        return cred.pid, cred.uid, cred.gid

    __all__.append("get_peer_pid_uid_gid")


elif sys.platform.startswith(("solaris", "illumos")):

    def get_peer_pid_uid_gid(sock: Union[socket.socket, int]) -> Tuple[Optional[int], int, int]:
        return peerucred._get_peer_pid_uid_gid(sock)  # pylint: disable=protected-access

    __all__.append("get_peer_pid_uid_gid")


get_peer_uid_gid.__doc__ = """
Get the UID and GID of the peer of the given socket.

Args:
    sock: The socket for which to obtain credentials.

Returns:
    A (uid, gid) tuple representing the credentials of the given socket's peer.

"""


if "get_peer_pid_uid_gid" in locals():
    get_peer_pid_uid_gid.__doc__ = """
Try to get the PID, UID, and GID of the peer of the given socket.

Args:
    sock: The socket for which to obtain credentials.

Returns:
    A (pid, uid, gid) tuple representing the credentials of the given socket's peer.

    WARNING: The PID returned may be None if the current version of the platform does not
    support retrieving the PID. For eximple, this is true on FreeBSD versions prior to
    FreeBSD 13. Callers should always check for the PID to be None.

"""
