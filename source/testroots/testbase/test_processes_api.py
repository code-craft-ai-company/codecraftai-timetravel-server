import pytest
from ccai.timetravelwebsite.restapis.versions.v1.feature.processes import (
    MOCK_PROCESSES, RequireAuth, list_processes, get_process, delete_process, refresh_process,
    disconnect_process, register_process, unregister_process, heartbeat_process
)

class MockRequest:
    def __init__(self, headers):
        self.headers = headers

def test_unauthenticated_request_returns_401():
    policy = RequireAuth()
    assert not policy.check_access(MockRequest({}))

def test_list_endpoint_with_pagination():
    MOCK_PROCESSES.clear()
    for i in range(15):
        MOCK_PROCESSES[f"proc-{i}"] = {
            "id": f"proc-{i}", "name": f"service-{i}", "state": "connected", "uptime_seconds": 120,
            "environment": {}, "arguments": [], "metadata": {}
        }

    data = list_processes(page=2, per_page=5)
    assert data['total'] == 15
    assert len(data['processes']) == 5
    assert data['processes'][0]['id'] == "proc-5"

def test_list_endpoint_with_state_filtering():
    MOCK_PROCESSES.clear()
    MOCK_PROCESSES["proc-1"] = {"id": "proc-1", "name": "A", "state": "connected", "uptime_seconds": 0, "environment": {}, "arguments": [], "metadata": {}}
    MOCK_PROCESSES["proc-2"] = {"id": "proc-2", "name": "B", "state": "disconnected", "uptime_seconds": 0, "environment": {}, "arguments": [], "metadata": {}}
    MOCK_PROCESSES["proc-3"] = {"id": "proc-3", "name": "C", "state": "connected", "uptime_seconds": 0, "environment": {}, "arguments": [], "metadata": {}}

    data = list_processes(state='disconnected')
    assert data['total'] == 1
    assert len(data['processes']) == 1
    assert data['processes'][0]['id'] == "proc-2"

def test_get_detail_returns_complete_process_info():
    MOCK_PROCESSES.clear()
    MOCK_PROCESSES["proc-1"] = {
        "id": "proc-1", "name": "A", "state": "connected", "uptime_seconds": 120,
        "environment": {"ENV": "test"}, "arguments": ["--run"], "metadata": {"v": "1"}
    }

    data = get_process("proc-1")
    assert data['environment'] == {"ENV": "test"}
    assert data['arguments'] == ["--run"]

def test_refresh_triggers_metadata_refresh():
    MOCK_PROCESSES.clear()
    MOCK_PROCESSES["proc-1"] = {"id": "proc-1"}

    data = refresh_process("proc-1")
    assert "Refresh triggered" in data['message']

def test_disconnect_changes_state():
    MOCK_PROCESSES.clear()
    MOCK_PROCESSES["proc-1"] = {"id": "proc-1", "state": "connected"}

    data = disconnect_process("proc-1")
    assert MOCK_PROCESSES["proc-1"]["state"] == "disconnected"

def test_delete_removes_disconnected_process():
    MOCK_PROCESSES.clear()
    MOCK_PROCESSES["proc-1"] = {"id": "proc-1", "state": "connected"}
    MOCK_PROCESSES["proc-2"] = {"id": "proc-2", "state": "disconnected"}

    with pytest.raises(ValueError, match="Can only delete disconnected"):
        delete_process("proc-1")

    data = delete_process("proc-2")
    assert "proc-2" not in MOCK_PROCESSES
