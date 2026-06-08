import pytest
import socket
import threading
import time
from ccai.timetravelserver.streamreceiver.session_lifecycle import StreamSessionLifecycle

class MockStorageBackend:
    def __init__(self):
        self.data = bytearray()
        self.flushed = False
        self.committed = False
        self.flush_count = 0

    def append(self, chunk):
        self.data.extend(chunk)

    def flush(self):
        self.flushed = True
        self.flush_count += 1

    def commit(self):
        self.committed = True

def test_session_full_lifecycle():
    server_sock, client_sock = socket.socketpair()
    storage = MockStorageBackend()

    session = StreamSessionLifecycle(server_sock, "token123", storage)

    # Run session in background
    session_thread = threading.Thread(target=session.run, daemon=True)
    session_thread.start()

    # Client sends data
    test_data = b"chunk1 chunk2"
    client_sock.sendall(test_data)

    time.sleep(0.1)

    # Client closes
    client_sock.close()

    # Session thread should exit
    session_thread.join(timeout=1.0)

    assert storage.data == test_data
    assert storage.committed == True

def test_session_flush_acknowledgement():
    server_sock, client_sock = socket.socketpair()
    storage = MockStorageBackend()

    session = StreamSessionLifecycle(server_sock, "token123", storage)

    session_thread = threading.Thread(target=session.run, daemon=True)
    session_thread.start()

    # Send data with flush marker
    client_sock.sendall(b"data FLUSH")

    # Client should receive ACK
    client_sock.settimeout(1.0)
    ack = client_sock.recv(1024)
    assert ack == b"ACK"

    time.sleep(0.1)
    assert b"data FLUSH" in storage.data
    assert storage.flushed == True

    client_sock.close()
    session_thread.join(timeout=1.0)
    assert storage.committed == True

def test_session_abrupt_disconnect():
    server_sock, client_sock = socket.socketpair()
    storage = MockStorageBackend()

    session = StreamSessionLifecycle(server_sock, "token123", storage)

    session_thread = threading.Thread(target=session.run, daemon=True)
    session_thread.start()

    client_sock.sendall(b"part1")
    time.sleep(0.1)

    # Simulate abrupt disconnect (RST)
    client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, b'\x01\x00\x00\x00\x00\x00\x00\x00')
    client_sock.close()

    session_thread.join(timeout=1.0)

    assert storage.data == b"part1"
    assert storage.committed == True # Should commit whatever it had

def test_session_partial_write_retry_logic():
    # We'll simulate partial writes from the socket's perspective.
    server_sock, client_sock = socket.socketpair()
    storage = MockStorageBackend()

    session = StreamSessionLifecycle(server_sock, "token123", storage)

    session_thread = threading.Thread(target=session.run, daemon=True)
    session_thread.start()

    client_sock.sendall(b"partial")
    time.sleep(0.1)
    client_sock.sendall(b"_write")

    time.sleep(0.1)
    client_sock.close()

    session_thread.join(timeout=1.0)
    assert storage.data == b"partial_write"
    assert storage.committed == True

def test_session_finalize_commits_data_atomically():
    server_sock, client_sock = socket.socketpair()
    storage = MockStorageBackend()

    session = StreamSessionLifecycle(server_sock, "token123", storage)

    session_thread = threading.Thread(target=session.run, daemon=True)
    session_thread.start()

    client_sock.sendall(b"data")
    time.sleep(0.1)

    assert storage.committed == False # Not committed yet

    client_sock.close()
    session_thread.join(timeout=1.0)

    assert storage.committed == True # Finalized and committed
