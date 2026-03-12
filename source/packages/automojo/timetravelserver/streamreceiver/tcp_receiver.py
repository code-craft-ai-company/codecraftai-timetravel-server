import socket
from typing import Callable, Any
from .base_receiver import BaseStreamReceiver

class TcpStreamReceiver(BaseStreamReceiver):
    def __init__(self, host: str, port: int, max_connections: int, auth_callback: Callable[[str], bool], session_factory: Callable[[socket.socket, str], Any]):
        super().__init__(max_connections, auth_callback, session_factory)
        self.host = host
        self.port = port

    def _create_and_bind_socket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        return sock
