import pytest
import socket
import os
import shutil
import struct
import tempfile
import time
from ccai.timetravelserver.streamreceiver.unix_receiver import UnixSocketStreamReceiver


@pytest.fixture
def sock_dir():
    """
    A SHORT directory for unix socket paths.

    AF_UNIX caps a socket path near 104 bytes on macOS, and pytest's
    `tmp_path` derives its directory from the test's NAME — so the
    longer-named tests in this module built paths over the limit and failed
    with 'AF_UNIX path too long' while the shortest one passed. That made it
    look like a receiver bug rather than a path-length one, and it only
    started happening when the repository moved to a deeper directory.

    mkdtemp under the system temp root is short and name-independent, so the
    limit cannot be reached by renaming a test.
    """
    path = tempfile.mkdtemp(prefix='ttr')
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)

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

def test_unix_receiver_accepts_connection(sock_dir):
    socket_path = os.path.join(sock_dir, 'test.sock')
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

def test_unix_receiver_cleans_up_stale_socket(sock_dir):
    socket_path = os.path.join(sock_dir, 'stale.sock')
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

def test_unix_receiver_cleans_up_on_stop(sock_dir):
    socket_path = os.path.join(sock_dir, 'cleanup.sock')
    auth_cb = lambda t: True
    session_factory = lambda s, t: MockSession(s, t)

    receiver = create_unix_receiver(socket_path, 10, auth_cb, session_factory)
    receiver.start()
    time.sleep(0.1)

    assert os.path.exists(socket_path)

    receiver.stop()
    assert not os.path.exists(socket_path)

def test_unix_receiver_auth_rejects(sock_dir):
    socket_path = os.path.join(sock_dir, 'auth.sock')
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
