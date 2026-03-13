import pytest
from flask import Flask
from flask_restx import Api
from automojo.timetravelwebsite.restapis.versions.v1.feature.portal_control import publish_namespaces, MOCK_PORTALS

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
    response = client.get('/api/v1/portals')
    assert response.status_code == 401

def test_list_portals_returns_correct_data(client, auth_headers):
    MOCK_PORTALS.clear()
    MOCK_PORTALS["p1"] = {"id": "p1", "name": "n1", "process_id": "proc-1", "is_active": True}
    MOCK_PORTALS["p2"] = {"id": "p2", "name": "n2", "process_id": "proc-1", "is_active": False}

    response = client.get('/api/v1/portals', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] == 2
    assert len(data['portals']) == 2

    response = client.get('/api/v1/portals?process_id=proc-1', headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()['total'] == 2

def test_activate_portal_success(client, auth_headers):
    MOCK_PORTALS.clear()
    MOCK_PORTALS["p1"] = {"id": "p1", "name": "n1", "process_id": "proc-1", "is_active": False}

    response = client.post('/api/v1/portals/p1/activate', headers=auth_headers)
    assert response.status_code == 200
    assert MOCK_PORTALS["p1"]["is_active"] is True

def test_deactivate_portal_success(client, auth_headers):
    MOCK_PORTALS.clear()
    MOCK_PORTALS["p1"] = {"id": "p1", "name": "n1", "process_id": "proc-1", "is_active": True}

    response = client.post('/api/v1/portals/p1/deactivate', headers=auth_headers)
    assert response.status_code == 200
    assert MOCK_PORTALS["p1"]["is_active"] is False

def test_bulk_activate_deactivate(client, auth_headers):
    MOCK_PORTALS.clear()
    MOCK_PORTALS["p1"] = {"id": "p1", "is_active": False}
    MOCK_PORTALS["p2"] = {"id": "p2", "is_active": False}
    MOCK_PORTALS["p3"] = {"id": "p3", "is_active": True}

    # Bulk activate
    response = client.post('/api/v1/portals/bulk',
                          json={"portal_ids": ["p1", "p2"], "action": "activate"},
                          headers=auth_headers)
    assert response.status_code == 200
    assert MOCK_PORTALS["p1"]["is_active"] is True
    assert MOCK_PORTALS["p2"]["is_active"] is True

    # Bulk deactivate
    response = client.post('/api/v1/portals/bulk',
                          json={"portal_ids": ["p1", "p3"], "action": "deactivate"},
                          headers=auth_headers)
    assert response.status_code == 200
    assert MOCK_PORTALS["p1"]["is_active"] is False
    assert MOCK_PORTALS["p3"]["is_active"] is False
