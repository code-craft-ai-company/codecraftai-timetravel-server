import pytest
from flask import Flask
from flask_restx import Api
from automojo.timetravelwebsite.restapis.versions.v1.feature.health import publish_namespaces, MOCK_HEALTH_STATUS

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

def test_health_endpoint_returns_correct_structure(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert 'version' in data
    assert 'uptime_seconds' in data
    assert 'components' in data
    assert 'database' in data['components']
    assert 'stream_receiver' in data['components']
    assert 'storage' in data['components']

def test_healthy_status_when_all_components_are_up(client):
    # Reset mock data
    MOCK_HEALTH_STATUS['components']['database']['status'] = 'up'
    MOCK_HEALTH_STATUS['components']['stream_receiver']['status'] = 'up'
    MOCK_HEALTH_STATUS['components']['storage']['status'] = 'up'

    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_degraded_status_when_a_component_has_issues(client):
    # Set one component to degraded
    MOCK_HEALTH_STATUS['components']['database']['status'] = 'degraded'

    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'degraded'

    # Reset it
    MOCK_HEALTH_STATUS['components']['database']['status'] = 'up'

def test_no_authentication_is_required(client):
    # Perform a request without any authentication headers
    response = client.get('/api/v1/health')
    assert response.status_code == 200
