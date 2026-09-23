import socket
import logging
from typing import Any

logger = logging.getLogger(__name__)

class StreamSessionLifecycle:
    def __init__(self, sock: socket.socket, token: str, storage_backend: Any, flow_controller: Any = None):
        self.sock = sock
        self.token = token
        self.storage_backend = storage_backend
        self.flow_controller = flow_controller
        self._running = False
        self._connection_id = str(id(sock))

        # We can assume handshake is already done and token validated
        # by the receiver before this session is instantiated and run.

    def run(self):
        """Manages the full lifecycle of the session."""
        self._running = True

        if self.flow_controller:
            self.flow_controller.register_connection(self._connection_id)

        try:
            self._receive_loop()
        except (socket.error, ConnectionResetError) as e:
            logger.info(f"Abrupt disconnect from client: {e}")
        except Exception as e:
            logger.error(f"Error during stream session: {e}", exc_info=True)
        finally:
            self._finalize()
            self._cleanup()

    def _receive_loop(self):
        """Reads chunks of data and appends to storage."""
        buffer_size = 0

        while self._running:
            try:
                # Set a small timeout to allow graceful shutdown checks
                self.sock.settimeout(1.0)
                chunk = self.sock.recv(4096)
                if not chunk:
                    break # Connection closed gracefully

                self.storage_backend.append(chunk)

                # Flow control integration
                if self.flow_controller:
                    buffer_size += len(chunk)
                    status = self.flow_controller.update_buffer_size(self._connection_id, buffer_size)

                    if status.value == "PAUSE":
                        self.sock.sendall(b"PAUSE")
                    elif status.value == "RESUME":
                        self.sock.sendall(b"RESUME")

                # Check for flush marker
                if b"FLUSH" in chunk:
                    self._handle_flush()
                    # Reset buffer size on flush as data is persisted
                    if self.flow_controller:
                        buffer_size = 0
                        status = self.flow_controller.update_buffer_size(self._connection_id, 0)
                        if status.value == "RESUME":
                            self.sock.sendall(b"RESUME")

            except socket.timeout:
                continue

    def _handle_flush(self):
        """Persists data and sends acknowledgement."""
        try:
            self.storage_backend.flush()
            # Send ACK back to client
            self.sock.sendall(b"ACK")
        except Exception as e:
            logger.error(f"Failed to flush storage: {e}")

    def _finalize(self):
        """Atomic commit of stored data."""
        try:
            self.storage_backend.commit()
        except Exception as e:
            logger.error(f"Failed to commit storage: {e}")

    def _cleanup(self):
        """Cleans up resources."""
        self._running = False

        if self.flow_controller:
            self.flow_controller.unregister_connection(self._connection_id)

        try:
            self.sock.close()
        except Exception:
            # Best-effort close during session cleanup; the peer may already have closed the socket.
            pass
