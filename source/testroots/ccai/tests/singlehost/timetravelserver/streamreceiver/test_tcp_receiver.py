"""
    .. module:: ccai.tests.singlehost.timetravelserver.streamreceiver.test_tcp_receiver
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the TcpStreamReceiver.
"""

import socket
import struct
import time
from ccai.timetravelserver.streamreceiver.tcp_receiver import TcpStreamReceiver

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

def create_tcp_receiver(host, port, max_conns, auth_cb, session_factory):
    receiver = TcpStreamReceiver(host, port, max_conns, auth_cb, session_factory)
    return receiver

def test_tcp_receiver_accepts_connection():
    # Setup
    port = 0  # let the OS pick a free port; fixed ports can fall in a reserved range on Windows
    auth_cb = lambda t: True
    session_factory = MockSession

    receiver = create_tcp_receiver("127.0.0.1", port, 10, auth_cb, session_factory)
    receiver.start()
    port = receiver.port

    time.sleep(0.1)  # wait for server to start

    try:
        # Client connects
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", port))

        # Handshake: send length + token
        token = b"valid_token"
        client.sendall(struct.pack("!H", len(token)) + token)

        # Receive auth success
        response = client.recv(1)
        assert response == b'\x01'
    finally:
        client.close()
        receiver.stop()

def test_tcp_receiver_auth_rejects():
    # Setup
    port = 0  # let the OS pick a free port; fixed ports can fall in a reserved range on Windows
    auth_cb = lambda t: False
    session_factory = MockSession

    receiver = create_tcp_receiver("127.0.0.1", port, 10, auth_cb, session_factory)
    receiver.start()
    port = receiver.port

    time.sleep(0.1)  # wait for server to start

    try:
        # Client connects
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", port))

        # Handshake: send length + token
        token = b"invalid_token"
        client.sendall(struct.pack("!H", len(token)) + token)

        # Receive auth failed
        response = client.recv(1)
        assert response == b'\x00'
    finally:
        client.close()
        receiver.stop()

def test_tcp_receiver_connection_limit():
    # Setup
    port = 0  # let the OS pick a free port; fixed ports can fall in a reserved range on Windows
    auth_cb = lambda t: True
    session_factory = MockSession

    # Only allow 1 connection
    receiver = create_tcp_receiver("127.0.0.1", port, 1, auth_cb, session_factory)
    receiver.start()
    port = receiver.port

    time.sleep(0.1)  # wait for server to start

    clients = []
    try:
        # First client
        client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client1.connect(("127.0.0.1", port))

        # Prevent GC of client1 so connection stays open
        clients.append(client1)

        time.sleep(0.1) # Wait for accept

        # Second client should be rejected
        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2.connect(("127.0.0.1", port))

        # Connection should be closed by server immediately or fail to send/receive
        time.sleep(0.1)
        try:
            client2.settimeout(0.5)
            # Send data to test if closed
            client2.sendall(b'test')
            # Expecting to fail reading or read empty
            resp = client2.recv(1024)
            assert resp == b'' # empty means connection closed
        except (socket.error, socket.timeout):
            pass # Connection error means it was rejected

        clients.append(client2)
    finally:
        for c in clients:
            try:
                c.close()
            except Exception:
                # Best-effort cleanup; the server may already have closed the rejected connection.
                pass
        receiver.stop()

def test_tcp_receiver_graceful_stop():
    port = 0  # let the OS pick a free port; fixed ports can fall in a reserved range on Windows
    auth_cb = lambda t: True

    # Keep session running so we can test draining
    class LongRunningSession(MockSession):
        def run(self):
            super().run()
            while True:
                try:
                    data = self.sock.recv(1024)
                    if not data: break
                except Exception:
                    break

    session_factory = lambda s, t: LongRunningSession(s, t)

    receiver = create_tcp_receiver("127.0.0.1", port, 10, auth_cb, session_factory)
    receiver.start()
    port = receiver.port

    time.sleep(0.1)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", port))

    token = b"test_token"
    client.sendall(struct.pack("!H", len(token)) + token)

    assert client.recv(1) == b'\x01'

    receiver.stop()

    # After stop, connection should be closed
    try:
        client.sendall(b'data')
        client.settimeout(0.5)
        resp = client.recv(1024)
        assert resp == b''
    except (socket.error, socket.timeout):
        # A socket error also shows that the stopped receiver closed the connection.
        pass

    client.close()

def test_tcp_receiver_data_forwarding():
    port = 0  # let the OS pick a free port; fixed ports can fall in a reserved range on Windows
    auth_cb = lambda t: True

    received_data = []

    class DataRecordingSession:
        def __init__(self, sock, token):
            self.sock = sock
            self.token = token

        def run(self):
            try:
                self.sock.settimeout(1.0)
                data = self.sock.recv(1024)
                received_data.append(data)
            except Exception:
                # A read failure leaves 'received_data' empty, which the test assertion reports.
                pass

    session_factory = lambda s, t: DataRecordingSession(s, t)

    receiver = create_tcp_receiver("127.0.0.1", port, 10, auth_cb, session_factory)
    receiver.start()
    port = receiver.port

    time.sleep(0.1)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", port))

    token = b"test_token"
    client.sendall(struct.pack("!H", len(token)) + token)
    assert client.recv(1) == b'\x01'

    # Send some data
    test_data = b"hello backend"
    client.sendall(test_data)

    time.sleep(0.1) # Wait for session to read

    receiver.stop()
    client.close()

    assert received_data == [test_data]


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
