import pytest
from flask import Flask

@pytest.fixture
def app():
    from automojo.timetravelwebsite.restapis import register_rest_blueprints

    app = Flask(__name__)
    register_rest_blueprints(app, "api")

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_headers():
    return {'Authorization': 'Bearer admin-token'}

@pytest.fixture
def user_headers():
    return {'Authorization': 'Bearer user-token'}

def test_unauthenticated_request(client):
    response = client.get('/api/v1/server-config/')
    assert response.status_code == 401

def test_non_admin_receives_403(client, user_headers):
    response = client.get('/api/v1/server-config/', headers=user_headers)
    assert response.status_code == 403

def test_get_all_configs(client, admin_headers):
    response = client.get('/api/v1/server-config/', headers=admin_headers)
    assert response.status_code == 200

    data = response.json
    assert 'retention_days' in data
    assert 'debug_logging' in data
    assert 'admin_email' in data

def test_put_updates_value(client, admin_headers):
    update_data = {"value": 45}
    response = client.put('/api/v1/server-config/retention_days', json=update_data, headers=admin_headers)
    assert response.status_code == 200
    assert response.json['message'] == "Configuration updated successfully"

    # Verify the update happened
    response = client.get('/api/v1/server-config/retention_days', headers=admin_headers)
    assert response.status_code == 200
    assert response.json['value'] == 45
    assert response.json['is_default'] is False

def test_put_rejects_invalid_type(client, admin_headers):
    # Try putting a string into an int field
    update_data = {"value": "forty-five"}
    response = client.put('/api/v1/server-config/retention_days', json=update_data, headers=admin_headers)
    assert response.status_code == 400
    assert "Invalid type" in response.json['message']
