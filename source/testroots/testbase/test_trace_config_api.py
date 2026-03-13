import pytest
from automojo.timetravelwebsite.restapis.versions.v1.feature.trace_config import (
    MOCK_TRACE_CONFIGS, RequireAuth, get_trace_config, update_trace_config
)

class MockRequest:
    def __init__(self, headers):
        self.headers = headers

def test_unauthenticated_request_returns_401():
    policy = RequireAuth()
    assert not policy.check_access(MockRequest({}))

def test_get_returns_configuration():
    MOCK_TRACE_CONFIGS.clear()
    MOCK_TRACE_CONFIGS["proc-1"] = {
        "process_id": "proc-1",
        "granularity": "call",
        "max_depth": 5,
        "track_variables": True
    }

    data = get_trace_config("proc-1")
    assert data["process_id"] == "proc-1"
    assert data["granularity"] == "call"
    assert data["max_depth"] == 5
    assert data["track_variables"] is True

def test_get_returns_default_for_unknown_process():
    MOCK_TRACE_CONFIGS.clear()
    data = get_trace_config("unknown-proc")
    assert data["process_id"] == "unknown-proc"
    assert data["granularity"] == "call"

def test_put_updates_configuration():
    MOCK_TRACE_CONFIGS.clear()
    MOCK_TRACE_CONFIGS["proc-1"] = {
        "process_id": "proc-1",
        "granularity": "call",
        "max_depth": 5,
        "track_variables": True
    }

    update_trace_config("proc-1", {"process_id": "proc-1", "granularity": "line", "max_depth": 10})
    assert MOCK_TRACE_CONFIGS["proc-1"]["granularity"] == "line"
    assert MOCK_TRACE_CONFIGS["proc-1"]["max_depth"] == 10

def test_invalid_granularity_value_returns_400():
    with pytest.raises(ValueError, match="Invalid granularity"):
        update_trace_config("proc-1", {"process_id": "proc-1", "granularity": "invalid-value"})
