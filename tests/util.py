import os
import socket
from typing import AnyStr, Tuple, Union


def sock_bind_connect_accept(
    path: Union[AnyStr, "os.PathLike[AnyStr]"],
) -> Tuple[socket.socket, socket.socket]:
    path = os.fspath(path)

    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listener.bind(path)
    listener.listen(1)
    listener.setblocking(False)

    cli = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    cli.connect(path)
    server_cli, _ = listener.accept()

    return cli, server_cli
