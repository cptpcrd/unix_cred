import os
import pathlib
import socket
import sys
from typing import Iterable

import pytest

from . import util

if sys.platform.startswith(("freebsd", "dragonfly", "darwin")):

    from unix_cred import xucred

    def check_grouplist(groups: Iterable[int]) -> None:
        if sys.platform.startswith("darwin"):
            # In macOS 10.5, Apple decided to change the behavior of getgroups() to make
            # it non-POSIX compliant and not an accurate reflection of the process's
            # supplementary group list. <sigh>
            assert set(groups) <= set(os.getgroups())
        else:
            # Check that the group list matches
            assert set(groups) == set(os.getgroups())

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

            check_grouplist(cred.groups)

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

            check_grouplist(cred.groups)

            if hasattr(cred, "pid"):
                assert cred.pid in (None, os.getpid())
