"""
    .. module:: ccai.tests.singlehost.timetravelserver.debugcontrol.test_command_dispatcher
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the CommandDispatcher JSON-lines client.
"""

import json
import socket
import threading
import time

from typing import Any, Dict

from ccai.testshared.assertions import assert_raises

from ccai.timetravelserver.debugcontrol.command_dispatcher import (
    CommandDispatcher,
    CommandError,
    CommandTimeoutError,
)


class MockRemoteControl:
    def __init__(self, responses: Dict[str, Any]):
        self.responses = responses
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("127.0.0.1", 0))
        self.server.listen(1)
        self.port = self.server.getsockname()[1]
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        self.requests = []

    def _run(self):
        while True:
            try:
                conn, _ = self.server.accept()
                with conn:
                    with conn.makefile("rw", encoding="utf-8") as f:
                        line = f.readline()
                        if not line:
                            continue
                        request = json.loads(line)
                        self.requests.append(request)

                        command = request.get("command")
                        response = self.responses.get(command, {"status": "error", "message": "Unknown command"})
                        f.write(json.dumps(response) + "\n")
                        f.flush()
            except Exception:
                break

    def close(self):
        self.server.close()


def test_successful_dispatch():
    responses = {
        "list_portals": {
            "status": "ok",
            "data": {
                "portals": [{"name": "test_portal", "is_active": True}]
            }
        }
    }
    remote = MockRemoteControl(responses)
    try:
        dispatcher = CommandDispatcher("test_token")
        response_data = dispatcher.dispatch(f"127.0.0.1:{remote.port}", "list_portals")

        assert len(remote.requests) == 1
        assert remote.requests[0]["command"] == "list_portals"
        assert remote.requests[0]["token"] == "test_token"
        assert response_data == {"portals": [{"name": "test_portal", "is_active": True}]}
    finally:
        remote.close()


def test_error_response():
    responses = {
        "failing_command": {
            "status": "error",
            "message": "Internal remote error"
        }
    }
    remote = MockRemoteControl(responses)
    try:
        dispatcher = CommandDispatcher("test_token")
        with assert_raises(CommandError) as exc_info:
            dispatcher.dispatch(f"127.0.0.1:{remote.port}", "failing_command")
        assert "Internal remote error" in str(exc_info.exception)
    finally:
        remote.close()


def test_connection_refused():
    # Bind a port, learn its number, then close it — connecting to a port
    # that was just released refuses deterministically on every platform.
    #
    # This used to dial 127.0.0.1:0. Port 0 means "any port" when BINDING;
    # connecting to it is not a refused connection but an invalid address,
    # and macOS answers EADDRNOTAVAIL — an OSError that is NOT a
    # ConnectionError, so the test failed here while passing on Linux.
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe.bind(("127.0.0.1", 0))
    closed_port = probe.getsockname()[1]
    probe.close()

    dispatcher = CommandDispatcher("test_token")
    with assert_raises(ConnectionError) as exc_info:
        dispatcher.dispatch(f"127.0.0.1:{closed_port}", "list_portals")
    assert "refused" in str(exc_info.exception).lower()


class SlowMockRemoteControl:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("127.0.0.1", 0))
        self.server.listen(1)
        self.port = self.server.getsockname()[1]
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def _run(self):
        while True:
            try:
                conn, _ = self.server.accept()
                with conn:
                    with conn.makefile("rw", encoding="utf-8") as f:
                        f.readline()
                        time.sleep(1) # sleep to trigger timeout
                        f.write('{"status": "ok", "data": {}}\n')
                        f.flush()
            except Exception:
                break

    def close(self):
        self.server.close()


def test_command_timeout():
    remote = SlowMockRemoteControl()
    try:
        dispatcher = CommandDispatcher("test_token", timeout_seconds=0.1)
        with assert_raises(CommandTimeoutError) as exc_info:
            dispatcher.dispatch(f"127.0.0.1:{remote.port}", "list_portals")
        assert "timed out" in str(exc_info.exception)
    finally:
        remote.close()


def test_close_connection_cleanup():
    dispatcher = CommandDispatcher("test_token")
    dispatcher.close() # Should not raise


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
