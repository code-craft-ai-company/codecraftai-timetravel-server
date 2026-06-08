import pytest
import socket
import os
import struct
import time
from ccai.timetravelserver.streamreceiver.unix_receiver import UnixSocketStreamReceiver

class MockSession:
    def __init__(self, sock, token):
        self.sock = sock
        self.token = token
        self.ran = False

    def run(self):
        self.ran = True
        try:
            self.sock.recv(1024)
        except Exception:
            pass

def create_unix_receiver(socket_path, max_conns, auth_cb, session_factory):
    receiver = UnixSocketStreamReceiver(socket_path, max_conns, auth_cb, session_factory)
    return receiver

def test_unix_receiver_accepts_connection(tmp_path):
    socket_path = str(tmp_path / "test.sock")
    auth_cb = lambda t: True
    session_factory = lambda s, t: MockSession(s, t)

    receiver = create_unix_receiver(socket_path, 10, auth_cb, session_factory)
    receiver.start()

    time.sleep(0.1)  # wait for server to start

    try:
        # Client connects
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(socket_path)

        # Handshake: send length + token
        token = b"valid_token"
        client.sendall(struct.pack("!H", len(token)) + token)

        # Receive auth success
        response = client.recv(1)
        assert response == b'\x01'
    finally:
        client.close()
        receiver.stop()

def test_unix_receiver_cleans_up_stale_socket(tmp_path):
    socket_path = str(tmp_path / "stale.sock")
    # Create a stale socket file
    with open(socket_path, 'w') as f:
        f.write('stale')

    auth_cb = lambda t: True
    session_factory = lambda s, t: MockSession(s, t)

    receiver = create_unix_receiver(socket_path, 10, auth_cb, session_factory)
    receiver.start()

    time.sleep(0.1)
    assert os.path.exists(socket_path)
    receiver.stop()

def test_unix_receiver_cleans_up_on_stop(tmp_path):
    socket_path = str(tmp_path / "cleanup.sock")
    auth_cb = lambda t: True
    session_factory = lambda s, t: MockSession(s, t)

    receiver = create_unix_receiver(socket_path, 10, auth_cb, session_factory)
    receiver.start()
    time.sleep(0.1)

    assert os.path.exists(socket_path)

    receiver.stop()
    assert not os.path.exists(socket_path)

def test_unix_receiver_auth_rejects(tmp_path):
    socket_path = str(tmp_path / "auth.sock")
    auth_cb = lambda t: False
    session_factory = lambda s, t: MockSession(s, t)

    receiver = create_unix_receiver(socket_path, 10, auth_cb, session_factory)
    receiver.start()

    time.sleep(0.1)

    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(socket_path)

        token = b"invalid_token"
        client.sendall(struct.pack("!H", len(token)) + token)

        response = client.recv(1)
        assert response == b'\x00'
    finally:
        client.close()
        receiver.stop()
