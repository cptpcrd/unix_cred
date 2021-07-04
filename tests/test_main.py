import os
import pathlib
import socket
import sys

import pytest

import unix_cred

from . import util


def test_get_peer_uid_gid(tmp_path: pathlib.Path) -> None:
    cli, server_cli = util.sock_bind_connect_accept(tmp_path / "sock")

    with cli, server_cli:
        assert unix_cred.get_peer_uid_gid(cli) == (os.geteuid(), os.getegid())
        assert unix_cred.get_peer_uid_gid(cli.fileno()) == (os.geteuid(), os.getegid())

        assert unix_cred.get_peer_uid_gid(server_cli) == (os.geteuid(), os.getegid())
        assert unix_cred.get_peer_uid_gid(server_cli.fileno()) == (os.geteuid(), os.getegid())

    with pytest.raises(OSError, match="Bad file descriptor"):
        unix_cred.get_peer_uid_gid(65535)


def test_get_peer_uid_gid_pair() -> None:
    sock_a, sock_b = socket.socketpair(socket.AF_UNIX)

    with sock_a, sock_b:
        assert unix_cred.get_peer_uid_gid(sock_a) == (os.geteuid(), os.getegid())
        assert unix_cred.get_peer_uid_gid(sock_a.fileno()) == (os.geteuid(), os.getegid())

        assert unix_cred.get_peer_uid_gid(sock_b) == (os.geteuid(), os.getegid())
        assert unix_cred.get_peer_uid_gid(sock_b.fileno()) == (os.geteuid(), os.getegid())


if sys.platform.startswith("darwin"):

    def test_get_peerpid(tmp_path: pathlib.Path) -> None:
        cli, server_cli = util.sock_bind_connect_accept(tmp_path / "sock")

        with cli, server_cli:
            assert unix_cred.get_peerpid(cli) == os.getpid()
            assert unix_cred.get_peerpid(cli.fileno()) == os.getpid()

            assert unix_cred.get_peerpid(server_cli) == os.getpid()
            assert unix_cred.get_peerpid(server_cli.fileno()) == os.getpid()

        with pytest.raises(OSError, match="Bad file descriptor"):
            unix_cred.get_peerpid(65535)

    def test_get_peerpid_pair() -> None:
        sock_a, sock_b = socket.socketpair(socket.AF_UNIX)

        with sock_a, sock_b:
            assert unix_cred.get_peerpid(sock_a) == os.getpid()
            assert unix_cred.get_peerpid(sock_a.fileno()) == os.getpid()

            assert unix_cred.get_peerpid(sock_b) == os.getpid()
            assert unix_cred.get_peerpid(sock_b.fileno()) == os.getpid()


if sys.platform.startswith(
    ("linux", "openbsd", "netbsd", "freebsd", "darwin", "solaris", "illumos")
):

    def test_get_peer_pid_uid_gid(tmp_path: pathlib.Path) -> None:
        cli, server_cli = util.sock_bind_connect_accept(tmp_path / "sock")

        with cli, server_cli:
            for (pid, uid, gid) in [
                unix_cred.get_peer_pid_uid_gid(cli),
                unix_cred.get_peer_pid_uid_gid(cli.fileno()),
                unix_cred.get_peer_pid_uid_gid(server_cli),
                unix_cred.get_peer_pid_uid_gid(server_cli.fileno()),
            ]:
                assert uid == os.geteuid()
                assert gid == os.getegid()
                assert pid in (None, os.getpid())

        with pytest.raises(OSError, match="Bad file descriptor"):
            unix_cred.get_peer_pid_uid_gid(65535)

    def test_get_peer_pid_uid_gid_pair() -> None:
        sock_a, sock_b = socket.socketpair(socket.AF_UNIX)

        with sock_a, sock_b:
            for (pid, uid, gid) in [
                unix_cred.get_peer_pid_uid_gid(sock_a),
                unix_cred.get_peer_pid_uid_gid(sock_a.fileno()),
                unix_cred.get_peer_pid_uid_gid(sock_b),
                unix_cred.get_peer_pid_uid_gid(sock_b.fileno()),
            ]:
                assert uid == os.geteuid()
                assert gid == os.getegid()
                assert pid in (None, os.getpid())
