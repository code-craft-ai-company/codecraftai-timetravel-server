import socket
import os
from typing import Callable, Any
from .base_receiver import BaseStreamReceiver

class UnixSocketStreamReceiver(BaseStreamReceiver):
    def __init__(self, socket_path: str, max_connections: int, auth_callback: Callable[[str], bool], session_factory: Callable[[socket.socket, str], Any]):
        super().__init__(max_connections, auth_callback, session_factory)
        self.socket_path = socket_path

    def _create_and_bind_socket(self) -> socket.socket:
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(self.socket_path)
        # Ensure correct permissions for unix socket
        os.chmod(self.socket_path, 0o600)
        return sock

    def _cleanup_socket(self):
        if os.path.exists(self.socket_path):
            try:
                os.remove(self.socket_path)
            except OSError:
                # Best-effort removal of the socket file; it may have been removed concurrently and a
                # stale file is removed again by the next bind.
                pass
