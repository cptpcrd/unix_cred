import os
import pathlib
import socket
import sys

import pytest

from . import util

if sys.platform.startswith(("linux", "openbsd", "netbsd")):

    from unix_cred import ucred

    def test_ucred(tmp_path: pathlib.Path) -> None:
        cli, server_cli = util.sock_bind_connect_accept(tmp_path / "sock")

        for cred in [
            ucred.get_ucred(cli),
            ucred.get_ucred(cli.fileno()),
            ucred.get_ucred(server_cli),
            ucred.get_ucred(server_cli.fileno()),
        ]:
            assert cred.uid == os.geteuid()
            assert cred.gid == os.getegid()
            assert cred.pid == os.getpid()

        with pytest.raises(OSError, match="Bad file descriptor"):
            ucred.get_ucred(65535)

    def test_ucred_pair() -> None:
        sock_a, sock_b = socket.socketpair(socket.AF_UNIX)

        for cred in [
            ucred.get_ucred(sock_a),
            ucred.get_ucred(sock_a.fileno()),
            ucred.get_ucred(sock_b),
            ucred.get_ucred(sock_b.fileno()),
        ]:
            assert cred.uid == os.geteuid()
            assert cred.gid == os.getegid()
            assert cred.pid == os.getpid()
