import os
import pathlib
import socket
import sys

import pytest

from . import util

if sys.platform.startswith(("freebsd", "dragonfly", "darwin")):

    from unix_cred import xucred

    def test_xucred(tmp_path: pathlib.Path) -> None:
        cli, server_cli = util.sock_bind_connect_accept(tmp_path / "sock")

        for cred in [
            xucred.get_xucred(cli),
            xucred.get_xucred(cli.fileno()),
            xucred.get_xucred(server_cli),
            xucred.get_xucred(server_cli.fileno()),
        ]:
            assert cred.uid == os.geteuid()
            assert cred.gid == os.getegid()
            assert set(cred.groups) <= set(os.getgroups())

            if hasattr(cred, "pid"):
                assert cred.pid in (None, os.getpid())

        with pytest.raises(OSError, match="Bad file descriptor"):
            xucred.get_xucred(65535)

    def test_xucred_pair() -> None:
        sock_a, sock_b = socket.socketpair(socket.AF_UNIX)

        for cred in [
            xucred.get_xucred(sock_a),
            xucred.get_xucred(sock_a.fileno()),
            xucred.get_xucred(sock_b),
            xucred.get_xucred(sock_b.fileno()),
        ]:
            assert cred.uid == os.geteuid()
            assert cred.gid == os.getegid()
            assert set(cred.groups) <= set(os.getgroups())

            if hasattr(cred, "pid"):
                assert cred.pid in (None, os.getpid())
