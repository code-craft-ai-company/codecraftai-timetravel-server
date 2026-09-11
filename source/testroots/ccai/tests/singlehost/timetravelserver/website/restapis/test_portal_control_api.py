"""
    .. module:: ccai.tests.singlehost.timetravelserver.website.restapis.test_portal_control_api
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the portal control REST API handlers.
"""

from ccai.timetravelwebsite.restapis.versions.v1.feature.portal_control import (
    MOCK_PORTALS, RequireAuth, list_portals, activate_portal, deactivate_portal, bulk_action_portals
)

class MockRequest:
    def __init__(self, headers):
        self.headers = headers

def test_unauthenticated_request_returns_401():
    policy = RequireAuth()
    assert not policy.check_access(MockRequest({}))

def test_list_portals_returns_correct_data():
    MOCK_PORTALS.clear()
    MOCK_PORTALS["p1"] = {"id": "p1", "name": "n1", "process_id": "proc-1", "is_active": True}
    MOCK_PORTALS["p2"] = {"id": "p2", "name": "n2", "process_id": "proc-1", "is_active": False}

    data = list_portals()
    assert data['total'] == 2
    assert len(data['portals']) == 2

    data = list_portals(process_id='proc-1')
    assert data['total'] == 2

def test_activate_portal_success():
    MOCK_PORTALS.clear()
    MOCK_PORTALS["p1"] = {"id": "p1", "name": "n1", "process_id": "proc-1", "is_active": False}

    activate_portal("p1")
    assert MOCK_PORTALS["p1"]["is_active"] is True

def test_deactivate_portal_success():
    MOCK_PORTALS.clear()
    MOCK_PORTALS["p1"] = {"id": "p1", "name": "n1", "process_id": "proc-1", "is_active": True}

    deactivate_portal("p1")
    assert MOCK_PORTALS["p1"]["is_active"] is False

def test_bulk_activate_deactivate():
    MOCK_PORTALS.clear()
    MOCK_PORTALS["p1"] = {"id": "p1", "is_active": False}
    MOCK_PORTALS["p2"] = {"id": "p2", "is_active": False}
    MOCK_PORTALS["p3"] = {"id": "p3", "is_active": True}

    # Bulk activate
    bulk_action_portals({"portal_ids": ["p1", "p2"], "action": "activate"})
    assert MOCK_PORTALS["p1"]["is_active"] is True
    assert MOCK_PORTALS["p2"]["is_active"] is True

    # Bulk deactivate
    bulk_action_portals({"portal_ids": ["p1", "p3"], "action": "deactivate"})
    assert MOCK_PORTALS["p1"]["is_active"] is False
    assert MOCK_PORTALS["p3"]["is_active"] is False


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
