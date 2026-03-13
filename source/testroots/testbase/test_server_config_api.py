import pytest
from automojo.timetravelwebsite.restapis.versions.v1.feature.server_config import (
    MOCK_SERVER_CONFIGS, RequireAdmin, get_all_server_configs,
    get_server_config, update_server_config
)

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

def test_get_all_configs():
    MOCK_SERVER_CONFIGS.clear()
    MOCK_SERVER_CONFIGS["test"] = {"value": 1, "type": "int", "description": "test", "is_default": True}

    data = get_all_server_configs()
    assert "test" in data
    assert data["test"]["value"] == 1

def test_put_updates_value():
    MOCK_SERVER_CONFIGS.clear()
    MOCK_SERVER_CONFIGS["retention"] = {"value": 30, "type": "int", "description": "test", "is_default": True}

    update_server_config("retention", {"value": 60})
    assert MOCK_SERVER_CONFIGS["retention"]["value"] == 60
    assert MOCK_SERVER_CONFIGS["retention"]["is_default"] is False

def test_put_rejects_invalid_type():
    MOCK_SERVER_CONFIGS.clear()
    MOCK_SERVER_CONFIGS["retention"] = {"value": 30, "type": "int", "description": "test", "is_default": True}

    with pytest.raises(ValueError, match="Invalid type"):
        update_server_config("retention", {"value": "60"})
