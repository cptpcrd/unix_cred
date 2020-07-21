# unix_cred

[![PyPI](https://img.shields.io/pypi/v/unix-cred)](https://pypi.org/project/unix-cred)
[![Python Versions](https://img.shields.io/pypi/pyversions/unix-cred)](https://pypi.org/project/unix-cred)
[![Documentation Status](https://readthedocs.org/projects/unix-cred/badge/?version=latest)](https://unix-cred.readthedocs.io/en/latest/)
[![GitHub Actions](https://github.com/cptpcrd/unix_cred/workflows/CI/badge.svg?branch=master&event=push)](https://github.com/cptpcrd/unix_cred/actions?query=workflow%3ACI+branch%3Amaster+event%3Apush)
[![Cirrus CI](https://api.cirrus-ci.com/github/cptpcrd/unix_cred.svg?branch=master)](https://cirrus-ci.com/github/cptpcrd/unix_cred)
[![codecov](https://codecov.io/gh/cptpcrd/unix_cred/branch/master/graph/badge.svg)](https://codecov.io/gh/cptpcrd/unix_cred)

A Python library that simplifies reading peer credentials from Unix domain sockets.

## Installation

```
$ pip install unix-cred
```

### Examples

```python
>>> import os
>>> import socket
>>> import unix_cred
>>> server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
>>> server.bind("/tmp/unix_cred-test")
>>> server.listen(1)
>>> cli = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
>>> cli.connect("/tmp/unix_cred-test")
>>> server_cli = server.accept()[0]
>>> # Check the peer credentials on each end against the current process's
>>> assert unix_cred.get_peer_uid_gid(cli) == (os.geteuid(), os.getegid())
>>> assert unix_cred.get_peer_uid_gid(server_cli) == (os.geteuid(), os.getegid())
>>> # Not supported on all systems
>>> # On some systems this function is not defined; on certain versions of other systems
>>> # it may return None for the PID
>>> assert unix_cred.get_peer_pid_uid_gid(cli) == (os.getpid(), os.geteuid(), os.getegid())
>>> assert unix_cred.get_peer_pid_uid_gid(server_cli) == (os.getpid(), os.geteuid(), os.getegid())
```
