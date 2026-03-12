from flask import request
from flask_restx import Namespace, Resource, fields

SERVER_CONFIG_NAMESPACE_PATH = "/server-config"
server_config_ns = Namespace("Server Configuration v1", description="Server Configuration API")

# Models for serialization
config_value_model = server_config_ns.model('ConfigValue', {
    'value': fields.Raw(description='Configuration value'),
    'type': fields.String(description='Value type (int, string, bool)'),
    'description': fields.String(description='Configuration description'),
    'is_default': fields.Boolean(description='Whether the value is the default')
})

# Mock Database
MOCK_SERVER_CONFIGS = {
    "retention_days": {"value": 30, "type": "int", "description": "Data retention period", "is_default": True},
    "debug_logging": {"value": False, "type": "bool", "description": "Enable debug logging", "is_default": True},
    "admin_email": {"value": "admin@example.com", "type": "string", "description": "Admin email contact", "is_default": False},
}

def require_admin(func):
    """Mock authentication and authorization decorator for admin role"""
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            server_config_ns.abort(401, "Unauthorized")

        # Mock checking role
        if auth_header == "Bearer user-token":
            server_config_ns.abort(403, "Forbidden: Admin role required")
        elif auth_header != "Bearer admin-token":
            server_config_ns.abort(401, "Unauthorized")

        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


@server_config_ns.route("/")
class ServerConfigList(Resource):
    @server_config_ns.doc(security='Bearer Auth')
    @require_admin
    def get(self):
        """Get all server configurations"""
        return MOCK_SERVER_CONFIGS, 200


@server_config_ns.route("/<string:key>")
class ServerConfigItem(Resource):
    @server_config_ns.doc(security='Bearer Auth')
    @require_admin
    @server_config_ns.marshal_with(config_value_model)
    def get(self, key):
        """Get a specific configuration value"""
        if key not in MOCK_SERVER_CONFIGS:
            server_config_ns.abort(404, "Configuration key not found")
        return MOCK_SERVER_CONFIGS[key]

    @server_config_ns.doc(security='Bearer Auth')
    @require_admin
    def put(self, key):
        """Update a specific configuration value"""
        if key not in MOCK_SERVER_CONFIGS:
            server_config_ns.abort(404, "Configuration key not found")

        data = request.json
        if not data or 'value' not in data:
            server_config_ns.abort(400, "Missing 'value' in request")

        new_value = data['value']
        expected_type = MOCK_SERVER_CONFIGS[key]['type']

        # Simple type validation
        if expected_type == 'int' and not isinstance(new_value, int) or isinstance(new_value, bool):
            server_config_ns.abort(400, "Invalid type, expected int")
        elif expected_type == 'bool' and not isinstance(new_value, bool):
            server_config_ns.abort(400, "Invalid type, expected bool")
        elif expected_type == 'string' and not isinstance(new_value, str):
            server_config_ns.abort(400, "Invalid type, expected string")

        # Update value
        MOCK_SERVER_CONFIGS[key]['value'] = new_value
        MOCK_SERVER_CONFIGS[key]['is_default'] = False

        return {"message": "Configuration updated successfully"}, 200

def publish_namespaces(version_prefix):
    ns_list = [
        (server_config_ns, "".join([version_prefix, SERVER_CONFIG_NAMESPACE_PATH]))
    ]
    return ns_list
