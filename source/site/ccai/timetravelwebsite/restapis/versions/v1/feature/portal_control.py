from typing import Dict, Any
from ccai.webworks.endpoints.restblueprint import RestBlueprint
from ccai.webworks.endpoints.accesspolicy import AccessPolicy

class RequireAuth(AccessPolicy):
    def check_access(self, request: Any) -> bool:
        auth_header = getattr(request, 'headers', {}).get('Authorization')
        return bool(auth_header)

class PortalControlAPI(RestBlueprint):
    base_path = "/portals"
    tags = ["Portal Control v1"]
    version = "1.0"
    access_policy = RequireAuth()

# Mock Database
MOCK_PORTALS = {
    "portal-1": {
        "id": "portal-1",
        "name": "core.user_login",
        "process_id": "proc-1",
        "is_active": True
    },
    "portal-2": {
        "id": "portal-2",
        "name": "billing.process_payment",
        "process_id": "proc-1",
        "is_active": False
    },
    "portal-3": {
        "id": "portal-3",
        "name": "search.query",
        "process_id": "proc-2",
        "is_active": True
    }
}


@PortalControlAPI.read(leaf="")
def list_portals(process_id: str = None) -> Dict[str, Any]:
    """List available portals"""
    filtered_portals = list(MOCK_PORTALS.values())
    if process_id:
        filtered_portals = [p for p in filtered_portals if p['process_id'] == process_id]

    return {
        'total': len(filtered_portals),
        'portals': filtered_portals
    }

@PortalControlAPI.create(leaf="/{id}/activate")
def activate_portal(id: str) -> Dict[str, Any]:
    """Activate a specific portal"""
    if id not in MOCK_PORTALS:
        raise ValueError("Portal not found")

    MOCK_PORTALS[id]['is_active'] = True
    return {"message": "Portal activated successfully"}

@PortalControlAPI.create(leaf="/{id}/deactivate")
def deactivate_portal(id: str) -> Dict[str, Any]:
    """Deactivate a specific portal"""
    if id not in MOCK_PORTALS:
        raise ValueError("Portal not found")

    MOCK_PORTALS[id]['is_active'] = False
    return {"message": "Portal deactivated successfully"}

@PortalControlAPI.create(leaf="/bulk")
def bulk_action_portals(body: Dict[str, Any]) -> Dict[str, Any]:
    """Perform bulk activation/deactivation of portals"""
    if not body or 'portal_ids' not in body or 'action' not in body:
        raise ValueError("Missing required fields")

    action = body['action']
    if action not in ['activate', 'deactivate']:
        raise ValueError("Invalid action, must be 'activate' or 'deactivate'")

    is_active = (action == 'activate')
    updated = 0

    for pid in body['portal_ids']:
        if pid in MOCK_PORTALS:
            MOCK_PORTALS[pid]['is_active'] = is_active
            updated += 1

    return {"message": f"Successfully updated {updated} portals"}
