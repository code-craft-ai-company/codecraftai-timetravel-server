import socket
from typing import Callable, Any
from .base_receiver import BaseStreamReceiver

class TcpStreamReceiver(BaseStreamReceiver):
    def __init__(self, host: str, port: int, max_connections: int, auth_callback: Callable[[str], bool], session_factory: Callable[[socket.socket, str], Any]):
        super().__init__(max_connections, auth_callback, session_factory)
        self.host = host
        self.port = port

    def _create_and_bind_socket(self) -> socket.socket:
        """
            Creates the listening socket and binds it to the configured host and port.  When the port is 0 the
            operating system picks a free port, and 'port' is updated to the one that was assigned.

            :returns: The bound socket.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        if self.port == 0:
            self.port = sock.getsockname()[1]
        return sock
