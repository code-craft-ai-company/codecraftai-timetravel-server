from typing import Dict, Any
from ccai.webworks.endpoints.restblueprint import RestBlueprint
from ccai.webworks.endpoints.accesspolicy import AccessPolicy

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

class ServerConfigAPI(RestBlueprint):
    base_path = "/server-config"
    tags = ["Server Configuration v1"]
    version = "1.0"
    access_policy = RequireAdmin()

# Mock Database
MOCK_SERVER_CONFIGS = {
    "retention_days": {"value": 30, "type": "int", "description": "Data retention period", "is_default": True},
    "debug_logging": {"value": False, "type": "bool", "description": "Enable debug logging", "is_default": True},
    "admin_email": {"value": "admin@example.com", "type": "string", "description": "Admin email contact", "is_default": False},
}

@ServerConfigAPI.read(leaf="")
def get_all_server_configs() -> Dict[str, Any]:
    """Get all server configurations"""
    return MOCK_SERVER_CONFIGS

@ServerConfigAPI.read(leaf="/{key}")
def get_server_config(key: str) -> Dict[str, Any]:
    """Get a specific configuration value"""
    if key not in MOCK_SERVER_CONFIGS:
        raise ValueError("Configuration key not found")
    return MOCK_SERVER_CONFIGS[key]

@ServerConfigAPI.update(leaf="/{key}")
def update_server_config(key: str, body: Dict[str, Any]) -> Dict[str, Any]:
    """Update a specific configuration value"""
    if key not in MOCK_SERVER_CONFIGS:
        raise ValueError("Configuration key not found")

    if not body or 'value' not in body:
        raise ValueError("Missing 'value' in request")

    new_value = body['value']
    expected_type = MOCK_SERVER_CONFIGS[key]['type']

    # Simple type validation
    if expected_type == 'int' and (not isinstance(new_value, int) or isinstance(new_value, bool)):
        raise ValueError("Invalid type, expected int")
    elif expected_type == 'bool' and not isinstance(new_value, bool):
        raise ValueError("Invalid type, expected bool")
    elif expected_type == 'string' and not isinstance(new_value, str):
        raise ValueError("Invalid type, expected string")

    # Update value
    MOCK_SERVER_CONFIGS[key]['value'] = new_value
    MOCK_SERVER_CONFIGS[key]['is_default'] = False

    return {"message": "Configuration updated successfully"}
