from flask import request
from flask_restx import Namespace, Resource, fields

CREDENTIALS_NAMESPACE_PATH = "/credentials"
credentials_ns = Namespace("Credential Management v1", description="Credential Management API")

# Models for serialization
credential_model = credentials_ns.model('Credential', {
    'id': fields.String(description='Credential ID'),
    'name': fields.String(description='Credential name'),
    'type': fields.String(description='Credential type (api_key, token)'),
    'status': fields.String(description='Status (active, revoked)'),
    'created_at': fields.String(description='Creation timestamp'),
    'last_used': fields.String(description='Last usage timestamp')
})

credential_create_model = credentials_ns.model('CredentialCreate', {
    'id': fields.String(description='Credential ID'),
    'name': fields.String(description='Credential name'),
    'token': fields.String(description='Plaintext token (only shown once)'),
})

credential_list_model = credentials_ns.model('CredentialList', {
    'total': fields.Integer(description='Total number of credentials'),
    'credentials': fields.List(fields.Nested(credential_model))
})

# Mock Database
MOCK_CREDENTIALS = {
    "1": {"id": "1", "name": "ci-server-key", "type": "api_key", "status": "active", "created_at": "2023-10-01T12:00:00Z", "last_used": "2023-10-24T12:00:00Z"},
    "2": {"id": "2", "name": "developer-token", "type": "token", "status": "revoked", "created_at": "2023-09-01T12:00:00Z", "last_used": "2023-09-15T12:00:00Z"},
}

def require_admin(func):
    """Mock authentication and authorization decorator for admin role"""
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            credentials_ns.abort(401, "Unauthorized")

        # Mock checking role
        if auth_header == "Bearer user-token":
            credentials_ns.abort(403, "Forbidden: Admin role required")
        elif auth_header != "Bearer admin-token":
            credentials_ns.abort(401, "Unauthorized")

        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


@credentials_ns.route("/")
class CredentialList(Resource):
    @credentials_ns.doc(security='Bearer Auth')
    @require_admin
    @credentials_ns.marshal_with(credential_list_model)
    def get(self):
        """List credentials"""
        creds = list(MOCK_CREDENTIALS.values())
        return {
            'total': len(creds),
            'credentials': creds
        }

    @credentials_ns.doc(security='Bearer Auth')
    @require_admin
    @credentials_ns.marshal_with(credential_create_model, code=201)
    def post(self):
        """Create a new credential"""
        data = request.json
        if not data or 'name' not in data or 'type' not in data:
            credentials_ns.abort(400, "Missing required fields (name, type)")

        new_id = str(len(MOCK_CREDENTIALS) + 1)
        new_token = f"tok-{new_id}-abcdef123456"

        MOCK_CREDENTIALS[new_id] = {
            "id": new_id,
            "name": data['name'],
            "type": data['type'],
            "status": "active",
            "created_at": "2023-10-24T12:00:00Z",
            "last_used": None
        }

        return {
            "id": new_id,
            "name": data['name'],
            "token": new_token
        }, 201


@credentials_ns.route("/<string:id>/rotate")
class CredentialRotate(Resource):
    @credentials_ns.doc(security='Bearer Auth')
    @require_admin
    @credentials_ns.marshal_with(credential_create_model)
    def post(self, id):
        """Rotate an existing credential"""
        if id not in MOCK_CREDENTIALS:
            credentials_ns.abort(404, "Credential not found")

        if MOCK_CREDENTIALS[id]['status'] != 'active':
            credentials_ns.abort(400, "Cannot rotate non-active credential")

        new_token = f"tok-{id}-newrotated987654"
        return {
            "id": id,
            "name": MOCK_CREDENTIALS[id]['name'],
            "token": new_token
        }, 200


@credentials_ns.route("/<string:id>/revoke")
class CredentialRevoke(Resource):
    @credentials_ns.doc(security='Bearer Auth')
    @require_admin
    def post(self, id):
        """Revoke a credential"""
        if id not in MOCK_CREDENTIALS:
            credentials_ns.abort(404, "Credential not found")

        if MOCK_CREDENTIALS[id]['status'] == 'revoked':
            credentials_ns.abort(400, "Credential is already revoked")

        MOCK_CREDENTIALS[id]['status'] = 'revoked'
        return {"message": "Credential revoked successfully"}, 200


@credentials_ns.route("/<string:id>")
class CredentialDetail(Resource):
    @credentials_ns.doc(security='Bearer Auth')
    @require_admin
    def delete(self, id):
        """Delete a revoked credential"""
        if id not in MOCK_CREDENTIALS:
            credentials_ns.abort(404, "Credential not found")

        if MOCK_CREDENTIALS[id]['status'] != 'revoked':
            credentials_ns.abort(400, "Can only delete revoked credentials")

        del MOCK_CREDENTIALS[id]
        return {"message": "Credential deleted successfully"}, 200

def publish_namespaces(version_prefix):
    ns_list = [
        (credentials_ns, "".join([version_prefix, CREDENTIALS_NAMESPACE_PATH]))
    ]
    return ns_list
