import os
import pathlib
import socket
import sys

import pytest

from . import util

if sys.platform.startswith(("solaris", "illumos")):

    from unix_cred import peerucred

    def test_peerucred(tmp_path: pathlib.Path) -> None:
        cli, server_cli = util.sock_bind_connect_accept(tmp_path / "sock")

        for cred in [
            peerucred.getpeerucred(cli),
            peerucred.getpeerucred(cli.fileno()),
            peerucred.getpeerucred(server_cli),
            peerucred.getpeerucred(server_cli.fileno()),
        ]:
            assert cred.pid == os.getpid()

            assert cred.ruid == os.getuid()
            assert cred.euid == os.geteuid()
            assert cred.suid == os.geteuid()

            assert cred.rgid == os.getgid()
            assert cred.egid == os.getegid()
            assert cred.sgid == os.getegid()

            assert set(cred.groups) <= set(os.getgroups())

        with pytest.raises(OSError, match="Bad file descriptor"):
            peerucred.getpeerucred(65535)

    def test_peerucred_pair() -> None:
        sock_a, sock_b = socket.socketpair(socket.AF_UNIX)

        for cred in [
            peerucred.getpeerucred(sock_a),
            peerucred.getpeerucred(sock_a.fileno()),
            peerucred.getpeerucred(sock_b),
            peerucred.getpeerucred(sock_b.fileno()),
        ]:
            assert cred.pid == os.getpid()

            assert cred.ruid == os.getuid()
            assert cred.euid == os.geteuid()
            assert cred.suid == os.geteuid()

            assert cred.rgid == os.getgid()
            assert cred.egid == os.getegid()
            assert cred.sgid == os.getegid()

            assert set(cred.groups) <= set(os.getgroups())
