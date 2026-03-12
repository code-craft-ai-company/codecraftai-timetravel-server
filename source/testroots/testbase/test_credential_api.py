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

@pytest.fixture(autouse=True)
def reset_mock_db():
    from automojo.timetravelwebsite.restapis.versions.v1.feature.credentials import MOCK_CREDENTIALS
    # Backup
    backup = {k: dict(v) for k, v in MOCK_CREDENTIALS.items()}
    yield
    # Restore
    MOCK_CREDENTIALS.clear()
    MOCK_CREDENTIALS.update(backup)

def test_unauthenticated_request(client):
    response = client.get('/api/v1/credentials/')
    assert response.status_code == 401

def test_non_admin_receives_403(client, user_headers):
    response = client.get('/api/v1/credentials/', headers=user_headers)
    assert response.status_code == 403

def test_list_does_not_expose_tokens(client, admin_headers):
    response = client.get('/api/v1/credentials/', headers=admin_headers)
    assert response.status_code == 200

    data = response.json
    assert data['total'] == 2
    for cred in data['credentials']:
        assert 'token' not in cred
        assert 'id' in cred
        assert 'name' in cred

def test_create_returns_plaintext_token(client, admin_headers):
    payload = {"name": "new-test-key", "type": "api_key"}
    response = client.post('/api/v1/credentials/', json=payload, headers=admin_headers)
    assert response.status_code == 201

    data = response.json
    assert data['name'] == "new-test-key"
    assert 'token' in data
    assert data['token'].startswith('tok-')

def test_rotate_returns_new_token(client, admin_headers):
    # Rotate active credential (id=1)
    response = client.post('/api/v1/credentials/1/rotate', headers=admin_headers)
    assert response.status_code == 200

    data = response.json
    assert data['id'] == "1"
    assert 'token' in data
    assert 'newrotated' in data['token']

def test_revoke_marks_credential_as_revoked(client, admin_headers):
    # Revoke active credential (id=1)
    response = client.post('/api/v1/credentials/1/revoke', headers=admin_headers)
    assert response.status_code == 200

    # Verify status changed
    response = client.get('/api/v1/credentials/', headers=admin_headers)
    creds = {c['id']: c for c in response.json['credentials']}
    assert creds['1']['status'] == 'revoked'

def test_delete_revoked_credential(client, admin_headers):
    # Try deleting active credential (should fail)
    response = client.delete('/api/v1/credentials/1', headers=admin_headers)
    assert response.status_code == 400

    # Try deleting revoked credential (id=2) (should succeed)
    response = client.delete('/api/v1/credentials/2', headers=admin_headers)
    assert response.status_code == 200
