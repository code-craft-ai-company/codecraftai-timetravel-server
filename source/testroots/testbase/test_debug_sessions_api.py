import pytest
from flask import Flask
from flask_restx import Api
from automojo.timetravelwebsite.restapis.versions.v1.feature.debug_sessions import publish_namespaces, MOCK_SESSIONS

@pytest.fixture
def app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='Test API')
    for ns_obj, ns_path in publish_namespaces("/api/v1"):
        api.add_namespace(ns_obj, ns_path)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}

def test_session_create_returns_session_id(client, auth_headers):
    MOCK_SESSIONS.clear()
    response = client.post('/api/v1/sessions', json={"process_id": "proc-test"}, headers=auth_headers)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["id"] == "sess-1"
    assert "sess-1" in MOCK_SESSIONS
    assert MOCK_SESSIONS["sess-1"]["process_id"] == "proc-test"

def test_list_sessions_with_filtering(client, auth_headers):
    MOCK_SESSIONS.clear()
    MOCK_SESSIONS["sess-1"] = {"id": "sess-1", "process_id": "p1", "status": "active", "start_time": "2023-10-25T10:00:00Z", "end_time": None}
    MOCK_SESSIONS["sess-2"] = {"id": "sess-2", "process_id": "p1", "status": "closed", "start_time": "2023-10-24T09:00:00Z", "end_time": "2023-10-24T11:00:00Z"}
    MOCK_SESSIONS["sess-3"] = {"id": "sess-3", "process_id": "p2", "status": "active", "start_time": "2023-10-25T10:00:00Z", "end_time": None}

    # Filter by process_id
    response = client.get('/api/v1/sessions?process_id=p1', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] == 2
    assert len(data['sessions']) == 2

    # Filter by status
    response = client.get('/api/v1/sessions?status=closed', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] == 1
    assert data['sessions'][0]['id'] == "sess-2"

def test_get_session_detail(client, auth_headers):
    MOCK_SESSIONS.clear()
    MOCK_SESSIONS["sess-1"] = {"id": "sess-1", "process_id": "p1", "status": "active", "start_time": "2023-10-25T10:00:00Z", "end_time": None}

    response = client.get('/api/v1/sessions/sess-1', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == "sess-1"
    assert data['process_id'] == "p1"
    assert data['status'] == "active"

def test_close_session(client, auth_headers):
    MOCK_SESSIONS.clear()
    MOCK_SESSIONS["sess-1"] = {"id": "sess-1", "process_id": "p1", "status": "active", "start_time": "2023-10-25T10:00:00Z", "end_time": None}

    response = client.post('/api/v1/sessions/sess-1/close', headers=auth_headers)
    assert response.status_code == 200
    assert MOCK_SESSIONS["sess-1"]["status"] == "closed"
    assert MOCK_SESSIONS["sess-1"]["end_time"] is not None
