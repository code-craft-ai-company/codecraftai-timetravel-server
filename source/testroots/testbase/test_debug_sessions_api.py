import pytest
from ccai.timetravelwebsite.restapis.versions.v1.feature.debug_sessions import (
    MOCK_SESSIONS, RequireAuth, list_sessions, create_session, get_session, close_session
)

class MockRequest:
    def __init__(self, headers):
        self.headers = headers

def test_unauthenticated_request_returns_401():
    policy = RequireAuth()
    assert not policy.check_access(MockRequest({}))

def test_session_create_returns_session_id():
    MOCK_SESSIONS.clear()
    data = create_session({"process_id": "proc-test"})
    assert "id" in data
    assert data["id"] == "sess-1"
    assert "sess-1" in MOCK_SESSIONS
    assert MOCK_SESSIONS["sess-1"]["process_id"] == "proc-test"

def test_list_sessions_with_filtering():
    MOCK_SESSIONS.clear()
    MOCK_SESSIONS["sess-1"] = {"id": "sess-1", "process_id": "p1", "status": "active", "start_time": "2023-10-25T10:00:00Z", "end_time": None}
    MOCK_SESSIONS["sess-2"] = {"id": "sess-2", "process_id": "p1", "status": "closed", "start_time": "2023-10-24T09:00:00Z", "end_time": "2023-10-24T11:00:00Z"}
    MOCK_SESSIONS["sess-3"] = {"id": "sess-3", "process_id": "p2", "status": "active", "start_time": "2023-10-25T10:00:00Z", "end_time": None}

    data = list_sessions(process_id='p1')
    assert data['total'] == 2
    assert len(data['sessions']) == 2

    data = list_sessions(status='closed')
    assert data['total'] == 1
    assert data['sessions'][0]['id'] == "sess-2"

def test_get_session_detail():
    MOCK_SESSIONS.clear()
    MOCK_SESSIONS["sess-1"] = {"id": "sess-1", "process_id": "p1", "status": "active", "start_time": "2023-10-25T10:00:00Z", "end_time": None}

    data = get_session("sess-1")
    assert data['id'] == "sess-1"
    assert data['process_id'] == "p1"
    assert data['status'] == "active"

def test_close_session():
    MOCK_SESSIONS.clear()
    MOCK_SESSIONS["sess-1"] = {"id": "sess-1", "process_id": "p1", "status": "active", "start_time": "2023-10-25T10:00:00Z", "end_time": None}

    close_session("sess-1")
    assert MOCK_SESSIONS["sess-1"]["status"] == "closed"
    assert MOCK_SESSIONS["sess-1"]["end_time"] is not None
