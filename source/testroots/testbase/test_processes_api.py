import pytest
from flask import Flask
from flask_restx import Api
from automojo.timetravelwebsite.restapis.versions.v1.feature.processes import publish_namespaces, MOCK_PROCESSES

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

def test_unauthenticated_request_returns_401(client):
    response = client.get('/api/v1/processes')
    assert response.status_code == 401

def test_list_endpoint_with_pagination(client, auth_headers):
    # Setup test data
    MOCK_PROCESSES.clear()
    for i in range(15):
        MOCK_PROCESSES[f"proc-{i}"] = {
            "id": f"proc-{i}", "name": f"service-{i}", "state": "connected", "uptime_seconds": 120,
            "environment": {}, "arguments": [], "metadata": {}
        }

    response = client.get('/api/v1/processes?page=2&per_page=5', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] == 15
    assert len(data['processes']) == 5
    assert data['processes'][0]['id'] == "proc-5"

def test_list_endpoint_with_state_filtering(client, auth_headers):
    MOCK_PROCESSES.clear()
    MOCK_PROCESSES["proc-1"] = {"id": "proc-1", "name": "A", "state": "connected", "uptime_seconds": 0, "environment": {}, "arguments": [], "metadata": {}}
    MOCK_PROCESSES["proc-2"] = {"id": "proc-2", "name": "B", "state": "disconnected", "uptime_seconds": 0, "environment": {}, "arguments": [], "metadata": {}}
    MOCK_PROCESSES["proc-3"] = {"id": "proc-3", "name": "C", "state": "connected", "uptime_seconds": 0, "environment": {}, "arguments": [], "metadata": {}}

    response = client.get('/api/v1/processes?state=disconnected', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] == 1
    assert len(data['processes']) == 1
    assert data['processes'][0]['id'] == "proc-2"

def test_get_detail_returns_complete_process_info(client, auth_headers):
    MOCK_PROCESSES.clear()
    MOCK_PROCESSES["proc-1"] = {
        "id": "proc-1", "name": "A", "state": "connected", "uptime_seconds": 120,
        "environment": {"ENV": "test"}, "arguments": ["--run"], "metadata": {"v": "1"}
    }

    response = client.get('/api/v1/processes/proc-1', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['environment'] == {"ENV": "test"}
    assert data['arguments'] == ["--run"]

def test_refresh_triggers_metadata_refresh(client, auth_headers):
    MOCK_PROCESSES.clear()
    MOCK_PROCESSES["proc-1"] = {"id": "proc-1"}

    response = client.post('/api/v1/processes/proc-1/refresh', headers=auth_headers)
    assert response.status_code == 200

def test_disconnect_changes_state(client, auth_headers):
    MOCK_PROCESSES.clear()
    MOCK_PROCESSES["proc-1"] = {"id": "proc-1", "state": "connected"}

    response = client.post('/api/v1/processes/proc-1/disconnect', headers=auth_headers)
    assert response.status_code == 200
    assert MOCK_PROCESSES["proc-1"]["state"] == "disconnected"

def test_delete_removes_disconnected_process(client, auth_headers):
    MOCK_PROCESSES.clear()
    MOCK_PROCESSES["proc-1"] = {"id": "proc-1", "state": "connected"}
    MOCK_PROCESSES["proc-2"] = {"id": "proc-2", "state": "disconnected"}

    response = client.delete('/api/v1/processes/proc-1', headers=auth_headers)
    assert response.status_code == 400  # Cannot delete connected

    response = client.delete('/api/v1/processes/proc-2', headers=auth_headers)
    assert response.status_code == 200
    assert "proc-2" not in MOCK_PROCESSES
