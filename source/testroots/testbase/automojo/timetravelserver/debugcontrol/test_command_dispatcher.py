import json
import socket
import threading
from typing import Any, Dict

import pytest

from automojo.timetravelserver.debugcontrol.command_dispatcher import (
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
        with pytest.raises(CommandError) as exc_info:
            dispatcher.dispatch(f"127.0.0.1:{remote.port}", "failing_command")
        assert "Internal remote error" in str(exc_info.value)
    finally:
        remote.close()


def test_connection_refused():
    dispatcher = CommandDispatcher("test_token")
    with pytest.raises(ConnectionError) as exc_info:
        dispatcher.dispatch("127.0.0.1:0", "list_portals")
    assert "refused" in str(exc_info.value).lower()


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
                        import time
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
        with pytest.raises(CommandTimeoutError) as exc_info:
            dispatcher.dispatch(f"127.0.0.1:{remote.port}", "list_portals")
        assert "timed out" in str(exc_info.value)
    finally:
        remote.close()

def test_close_connection_cleanup():
    dispatcher = CommandDispatcher("test_token")
    dispatcher.close() # Should not raise
