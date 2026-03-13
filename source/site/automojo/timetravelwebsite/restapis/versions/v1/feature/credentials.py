from typing import Dict, Any
from automojo.webworks.endpoints.restblueprint import RestBlueprint
from automojo.webworks.endpoints.accesspolicy import AccessPolicy

class RequireAdmin(AccessPolicy):
    def check_access(self, request: Any) -> bool:
        auth_header = getattr(request, 'headers', {}).get('Authorization')
        if not auth_header:
            raise ValueError("Unauthorized")
        if auth_header == "Bearer user-token":
            raise ValueError("Forbidden: Admin role required")
        elif auth_header != "Bearer admin-token":
            raise ValueError("Unauthorized")
        return True

class CredentialAPI(RestBlueprint):
    base_path = "/credentials"
    tags = ["Credential Management v1"]
    version = "1.0"
    access_policy = RequireAdmin()

# Mock Database
MOCK_CREDENTIALS = {
    "1": {"id": "1", "name": "ci-server-key", "type": "api_key", "status": "active", "created_at": "2023-10-01T12:00:00Z", "last_used": "2023-10-24T12:00:00Z"},
    "2": {"id": "2", "name": "developer-token", "type": "token", "status": "revoked", "created_at": "2023-09-01T12:00:00Z", "last_used": "2023-09-15T12:00:00Z"},
}

@CredentialAPI.read(leaf="")
def list_credentials() -> Dict[str, Any]:
    """List credentials"""
    creds = list(MOCK_CREDENTIALS.values())
    return {
        'total': len(creds),
        'credentials': creds
    }

@CredentialAPI.create(leaf="")
def create_credential(body: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new credential"""
    if not body or 'name' not in body or 'type' not in body:
        raise ValueError("Missing required fields (name, type)")

    new_id = str(len(MOCK_CREDENTIALS) + 1)
    new_token = f"tok-{new_id}-abcdef123456"

    MOCK_CREDENTIALS[new_id] = {
        "id": new_id,
        "name": body['name'],
        "type": body['type'],
        "status": "active",
        "created_at": "2023-10-24T12:00:00Z",
        "last_used": None
    }

    return {
        "id": new_id,
        "name": body['name'],
        "token": new_token
    }

@CredentialAPI.create(leaf="/{id}/rotate")
def rotate_credential(id: str) -> Dict[str, Any]:
    """Rotate an existing credential"""
    if id not in MOCK_CREDENTIALS:
        raise ValueError("Credential not found")

    if MOCK_CREDENTIALS[id]['status'] != 'active':
        raise ValueError("Cannot rotate non-active credential")

    new_token = f"tok-{id}-newrotated987654"
    return {
        "id": id,
        "name": MOCK_CREDENTIALS[id]['name'],
        "token": new_token
    }

@CredentialAPI.create(leaf="/{id}/revoke")
def revoke_credential(id: str) -> Dict[str, Any]:
    """Revoke a credential"""
    if id not in MOCK_CREDENTIALS:
        raise ValueError("Credential not found")

    if MOCK_CREDENTIALS[id]['status'] == 'revoked':
        raise ValueError("Credential is already revoked")

    MOCK_CREDENTIALS[id]['status'] = 'revoked'
    return {"message": "Credential revoked successfully"}

@CredentialAPI.delete(leaf="/{id}")
def delete_credential(id: str) -> Dict[str, Any]:
    """Delete a revoked credential"""
    if id not in MOCK_CREDENTIALS:
        raise ValueError("Credential not found")

    if MOCK_CREDENTIALS[id]['status'] != 'revoked':
        raise ValueError("Can only delete revoked credentials")

    del MOCK_CREDENTIALS[id]
    return {"message": "Credential deleted successfully"}
