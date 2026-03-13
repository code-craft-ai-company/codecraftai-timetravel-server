from typing import Dict, Any, List
from automojo.webworks.endpoints.restblueprint import RestBlueprint
from automojo.webworks.endpoints.accesspolicy import AccessPolicy

# Very basic authentication policy implementation since we don't have the full webworks auth context
class RequireAuth(AccessPolicy):
    def check_access(self, request: Any) -> bool:
        auth_header = getattr(request, 'headers', {}).get('Authorization')
        return bool(auth_header)

class ProcessAPI(RestBlueprint):
    base_path = "/processes"
    tags = ["Process Management v1"]
    version = "1.0"
    access_policy = RequireAuth()

# Mock Database
MOCK_PROCESSES = {
    "proc-1": {
        "id": "proc-1",
        "name": "service-a",
        "state": "connected",
        "uptime_seconds": 120,
        "environment": {"ENV": "production"},
        "arguments": ["--config", "config.yml"],
        "metadata": {"version": "1.0.0"}
    },
    "proc-2": {
        "id": "proc-2",
        "name": "service-b",
        "state": "disconnected",
        "uptime_seconds": 3600,
        "environment": {"ENV": "staging"},
        "arguments": ["--debug"],
        "metadata": {"version": "1.1.0"}
    }
}

# The request parameter types in webworks would normally be matched against function arguments
# Assuming query params are passed to kwargs or can be accessed through the request context.
# We will just write basic function signatures that return dicts.

@ProcessAPI.read(leaf="")
def list_processes(state: str = None, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """List processes with pagination, filtering, sorting"""
    filtered_processes = list(MOCK_PROCESSES.values())
    if state:
        filtered_processes = [p for p in filtered_processes if p['state'] == state]

    start = (page - 1) * per_page
    end = start + per_page
    paginated_processes = filtered_processes[start:end]

    return {
        'total': len(filtered_processes),
        'processes': paginated_processes
    }

@ProcessAPI.read(leaf="/{id}")
def get_process(id: str) -> Dict[str, Any]:
    """Get process detail"""
    if id not in MOCK_PROCESSES:
        raise ValueError("Process not found") # Will be caught by webworks error handlers
    return MOCK_PROCESSES[id]

@ProcessAPI.delete(leaf="/{id}")
def delete_process(id: str) -> Dict[str, Any]:
    """Delete disconnected process"""
    if id not in MOCK_PROCESSES:
        raise ValueError("Process not found")

    if MOCK_PROCESSES[id]['state'] != 'disconnected':
        raise ValueError("Can only delete disconnected processes")

    del MOCK_PROCESSES[id]
    return {"message": "Process deleted successfully"}

@ProcessAPI.create(leaf="/{id}/refresh")
def refresh_process(id: str) -> Dict[str, Any]:
    """Trigger metadata refresh"""
    if id not in MOCK_PROCESSES:
        raise ValueError("Process not found")

    return {"message": "Refresh triggered successfully"}

@ProcessAPI.create(leaf="/{id}/disconnect")
def disconnect_process(id: str) -> Dict[str, Any]:
    """Disconnect a process"""
    if id not in MOCK_PROCESSES:
        raise ValueError("Process not found")

    MOCK_PROCESSES[id]['state'] = 'disconnected'
    return {"message": "Process disconnected successfully"}

@ProcessAPI.create(leaf="/register")
def register_process(body: Dict[str, Any]) -> Dict[str, Any]:
    """Register a new process"""
    if not body or 'name' not in body:
        raise ValueError("Missing required fields")

    new_id = f"proc-{len(MOCK_PROCESSES) + 1}"
    MOCK_PROCESSES[new_id] = {
        "id": new_id,
        "name": body['name'],
        "state": "connected",
        "uptime_seconds": 0,
        "environment": body.get('environment', {}),
        "arguments": body.get('arguments', []),
        "metadata": {}
    }
    # Return 201 equivalent dict (assuming webworks wraps this)
    return {"id": new_id, "message": "Process registered successfully"}

@ProcessAPI.create(leaf="/{id}/unregister")
def unregister_process(id: str) -> Dict[str, Any]:
    """Unregister a process"""
    if id not in MOCK_PROCESSES:
        raise ValueError("Process not found")

    MOCK_PROCESSES[id]['state'] = 'disconnected'
    return {"message": "Process unregistered successfully"}

@ProcessAPI.create(leaf="/{id}/heartbeat")
def heartbeat_process(id: str) -> Dict[str, Any]:
    """Send heartbeat for a process"""
    if id not in MOCK_PROCESSES:
        raise ValueError("Process not found")

    MOCK_PROCESSES[id]['state'] = 'connected'
    return {"message": "Heartbeat received"}
