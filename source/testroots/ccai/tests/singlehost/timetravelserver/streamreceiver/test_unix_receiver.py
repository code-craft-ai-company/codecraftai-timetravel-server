"""
    .. module:: ccai.tests.singlehost.timetravelserver.streamreceiver.test_unix_receiver
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the UnixSocketStreamReceiver.
"""

import socket
import os
import struct
import time

from ccai.testshared.unixsockets import require_unix_domain_sockets, temporary_socket_directory

from ccai.timetravelserver.streamreceiver.unix_receiver import UnixSocketStreamReceiver

# Unix domain sockets do not exist on Windows: `socket.AF_UNIX` is absent there,
# so every test in this module skips (via `require_unix_domain_sockets`) rather
# than failing inside the receiver.  The product module itself imports cleanly on
# Windows; only binding needs AF_UNIX, which is why the guard is on the tests and
# not on the import.
#
# Every test also takes its socket path from `temporary_socket_directory`, a SHORT
# mkdtemp directory: AF_UNIX caps a socket path near 104 bytes on macOS and a
# test-name-derived directory can push the longer-named tests over that limit.

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
            # The mock session only blocks until data arrives or the connection closes; a socket error
            # simply ends the mock session.
            pass

def create_unix_receiver(socket_path, max_conns, auth_cb, session_factory):
    receiver = UnixSocketStreamReceiver(socket_path, max_conns, auth_cb, session_factory)
    return receiver

def test_unix_receiver_accepts_connection():
    require_unix_domain_sockets()

    with temporary_socket_directory() as sock_dir:
        socket_path = os.path.join(sock_dir, 'test.sock')
        auth_cb = lambda t: True
        session_factory = MockSession

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

def test_unix_receiver_cleans_up_stale_socket():
    require_unix_domain_sockets()

    with temporary_socket_directory() as sock_dir:
        socket_path = os.path.join(sock_dir, 'stale.sock')
        # Create a stale socket file
        with open(socket_path, 'w') as f:
            f.write('stale')

        auth_cb = lambda t: True
        session_factory = MockSession

        receiver = create_unix_receiver(socket_path, 10, auth_cb, session_factory)
        receiver.start()

        time.sleep(0.1)
        assert os.path.exists(socket_path)
        receiver.stop()

def test_unix_receiver_cleans_up_on_stop():
    require_unix_domain_sockets()

    with temporary_socket_directory() as sock_dir:
        socket_path = os.path.join(sock_dir, 'cleanup.sock')
        auth_cb = lambda t: True
        session_factory = MockSession

        receiver = create_unix_receiver(socket_path, 10, auth_cb, session_factory)
        receiver.start()
        time.sleep(0.1)

        assert os.path.exists(socket_path)

        receiver.stop()
        assert not os.path.exists(socket_path)

def test_unix_receiver_auth_rejects():
    require_unix_domain_sockets()

    with temporary_socket_directory() as sock_dir:
        socket_path = os.path.join(sock_dir, 'auth.sock')
        auth_cb = lambda t: False
        session_factory = MockSession

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


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
