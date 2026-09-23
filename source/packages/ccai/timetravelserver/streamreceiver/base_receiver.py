import socket
import threading
import logging
import struct
from typing import Callable, Dict, Any, Optional

logger = logging.getLogger(__name__)

class BaseStreamReceiver:
    def __init__(self, max_connections: int, auth_callback: Callable[[str], bool], session_factory: Callable[[socket.socket, str], Any]):
        self.max_connections = max_connections
        self.auth_callback = auth_callback
        self.session_factory = session_factory

        self._server_socket: Optional[socket.socket] = None
        self._accept_thread: Optional[threading.Thread] = None
        self._running = False
        self._connections: Dict[socket.socket, threading.Thread] = {}
        self._connections_lock = threading.Lock()

    def start(self):
        self._server_socket = self._create_and_bind_socket()
        self._server_socket.listen()

        self._running = True
        self._accept_thread = threading.Thread(target=self._accept_loop, daemon=True)
        self._accept_thread.start()

    def stop(self):
        self._running = False
        if self._server_socket:
            try:
                self._server_socket.close()
            except Exception:
                # Best-effort close during shutdown; a failure to close the listening socket must not
                # prevent the socket file and client connections from being cleaned up.
                pass
            self._cleanup_socket()

        if self._accept_thread and self._accept_thread.is_alive():
            self._accept_thread.join(timeout=1.0)

        with self._connections_lock:
            for conn in list(self._connections.keys()):
                try:
                    conn.shutdown(socket.SHUT_RDWR)
                    conn.close()
                except Exception:
                    # Best-effort shutdown; the peer may already have closed the connection, and one
                    # failing connection must not prevent the remaining connections from being closed.
                    pass
            self._connections.clear()

    def _create_and_bind_socket(self) -> socket.socket:
        raise NotImplementedError

    def _cleanup_socket(self):
        pass

    def _accept_loop(self):
        while self._running:
            try:
                client_sock, addr = self._server_socket.accept()
            except Exception as e:
                if not self._running:
                    break
                logger.error(f"Error accepting connection: {e}")
                continue

            with self._connections_lock:
                if len(self._connections) >= self.max_connections:
                    logger.warning(f"Connection limit reached, rejecting {addr}")
                    try:
                        client_sock.close()
                    except Exception:
                        # Best-effort close of a rejected connection; a failure here must not stop the
                        # accept loop from serving further connections.
                        pass
                    continue

                client_thread = threading.Thread(
                    target=self._handle_connection_wrapper,
                    args=(client_sock, addr),
                    daemon=True
                )
                self._connections[client_sock] = client_thread
                client_thread.start()

    def _handle_connection_wrapper(self, client_sock: socket.socket, addr: tuple):
        try:
            self._handle_connection(client_sock, addr)
        except Exception as e:
            logger.error(f"Error handling connection from {addr}: {e}")
        finally:
            try:
                client_sock.close()
            except Exception:
                # Best-effort close in cleanup; the connection may already be closed and a failure here
                # must not prevent the connection from being removed from the registry.
                pass

            with self._connections_lock:
                if client_sock in self._connections:
                    del self._connections[client_sock]

    def _read_exactly(self, sock: socket.socket, n: int) -> Optional[bytes]:
        data = bytearray()
        while len(data) < n:
            try:
                packet = sock.recv(n - len(data))
                if not packet:
                    return None
                data.extend(packet)
            except Exception:
                return None
        return bytes(data)

    def _handle_connection(self, client_sock: socket.socket, addr: tuple):
        # Format for handshake:
        # [2 bytes length][token bytes]
        length_bytes = self._read_exactly(client_sock, 2)
        if not length_bytes:
            return

        token_len = struct.unpack("!H", length_bytes)[0]
        token_bytes = self._read_exactly(client_sock, token_len)
        if not token_bytes:
            return

        token = token_bytes.decode('utf-8')

        if not self.auth_callback(token):
            logger.warning(f"Authentication failed for {addr}")
            # Send auth failed response
            client_sock.sendall(b'\x00')
            return

        # Send auth success response
        client_sock.sendall(b'\x01')

        # Hand off to session
        session = self.session_factory(client_sock, token)
        session.run()
