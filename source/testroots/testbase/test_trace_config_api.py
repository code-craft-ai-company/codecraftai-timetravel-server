import pytest
from flask import Flask
from flask_restx import Api
from automojo.timetravelwebsite.restapis.versions.v1.feature.trace_config import publish_namespaces, MOCK_TRACE_CONFIGS

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
    response = client.get('/api/v1/trace-config/proc-1')
    assert response.status_code == 401

def test_get_returns_configuration(client, auth_headers):
    MOCK_TRACE_CONFIGS.clear()
    MOCK_TRACE_CONFIGS["proc-1"] = {
        "process_id": "proc-1",
        "granularity": "call",
        "max_depth": 5,
        "track_variables": True
    }

    response = client.get('/api/v1/trace-config/proc-1', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["process_id"] == "proc-1"
    assert data["granularity"] == "call"
    assert data["max_depth"] == 5
    assert data["track_variables"] is True

def test_get_returns_default_for_unknown_process(client, auth_headers):
    MOCK_TRACE_CONFIGS.clear()
    response = client.get('/api/v1/trace-config/unknown-proc', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["process_id"] == "unknown-proc"
    assert data["granularity"] == "call"

def test_put_updates_configuration(client, auth_headers):
    MOCK_TRACE_CONFIGS.clear()
    MOCK_TRACE_CONFIGS["proc-1"] = {
        "process_id": "proc-1",
        "granularity": "call",
        "max_depth": 5,
        "track_variables": True
    }

    response = client.put('/api/v1/trace-config/proc-1',
                         json={"process_id": "proc-1", "granularity": "line", "max_depth": 10},
                         headers=auth_headers)
    assert response.status_code == 200
    assert MOCK_TRACE_CONFIGS["proc-1"]["granularity"] == "line"
    assert MOCK_TRACE_CONFIGS["proc-1"]["max_depth"] == 10

def test_invalid_granularity_value_returns_400(client, auth_headers):
    response = client.put('/api/v1/trace-config/proc-1',
                         json={"process_id": "proc-1", "granularity": "invalid-value"},
                         headers=auth_headers)
    assert response.status_code == 400
