import contextlib
import errno
import os
import socket
from typing import Iterator, Union


def build_oserror(
    eno: int, filename: Union[str, bytes, None] = None, filename2: Union[str, bytes, None] = None,
) -> OSError:
    return OSError(eno, os.strerror(eno), filename, None, filename2)


@contextlib.contextmanager
def with_socket_or_fd(sock: Union[socket.socket, int]) -> Iterator[socket.socket]:
    if isinstance(sock, int):
        try:
            sock_obj = socket.socket(fileno=sock)
        except OSError as ex:
            if ex.errno == errno.EINVAL:
                sock_obj = socket.socket(proto=0, fileno=sock)
            else:
                raise

        try:
            yield sock_obj
        finally:
            sock_obj.detach()
    else:
        yield sock
