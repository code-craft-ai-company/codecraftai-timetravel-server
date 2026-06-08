import pytest
from ccai.timetravelwebsite.restapis.versions.v1.feature.credentials import (
    MOCK_CREDENTIALS, RequireAdmin, list_credentials, create_credential,
    rotate_credential, revoke_credential, delete_credential
)

# Test access policy manually as the routing framework isn't invoked here
class MockRequest:
    def __init__(self, headers):
        self.headers = headers

def test_unauthenticated_request():
    policy = RequireAdmin()
    with pytest.raises(ValueError, match="Unauthorized"):
        policy.check_access(MockRequest({}))

def test_non_admin_receives_403():
    policy = RequireAdmin()
    with pytest.raises(ValueError, match="Forbidden"):
        policy.check_access(MockRequest({"Authorization": "Bearer user-token"}))

def test_list_does_not_expose_tokens():
    MOCK_CREDENTIALS.clear()
    MOCK_CREDENTIALS["1"] = {"id": "1", "name": "test", "type": "api_key", "status": "active", "created_at": "now", "last_used": None}

    data = list_credentials()
    assert data['total'] == 1
    assert 'token' not in data['credentials'][0]

def test_create_returns_plaintext_token():
    MOCK_CREDENTIALS.clear()
    data = create_credential({"name": "new-key", "type": "token"})
    assert "token" in data
    assert "tok-1-abcdef123456" in data["token"]

def test_rotate_returns_new_token():
    MOCK_CREDENTIALS.clear()
    MOCK_CREDENTIALS["1"] = {"id": "1", "name": "test", "type": "api_key", "status": "active", "created_at": "now", "last_used": None}

    data = rotate_credential("1")
    assert "newrotated" in data["token"]

def test_revoke_marks_credential_as_revoked():
    MOCK_CREDENTIALS.clear()
    MOCK_CREDENTIALS["1"] = {"id": "1", "name": "test", "type": "api_key", "status": "active", "created_at": "now", "last_used": None}

    revoke_credential("1")
    assert MOCK_CREDENTIALS["1"]["status"] == "revoked"

def test_delete_revoked_credential():
    MOCK_CREDENTIALS.clear()
    MOCK_CREDENTIALS["1"] = {"id": "1", "name": "test", "type": "api_key", "status": "revoked", "created_at": "now", "last_used": None}

    delete_credential("1")
    assert "1" not in MOCK_CREDENTIALS
