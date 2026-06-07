from typing import Dict, Any
from ccai.webworks.endpoints.restblueprint import RestBlueprint
from ccai.webworks.endpoints.accesspolicy import AccessPolicy

class RequireAuth(AccessPolicy):
    def check_access(self, request: Any) -> bool:
        auth_header = getattr(request, 'headers', {}).get('Authorization')
        return bool(auth_header)

class DebugSessionAPI(RestBlueprint):
    base_path = "/sessions"
    tags = ["Debug Sessions v1"]
    version = "1.0"
    access_policy = RequireAuth()

# Mock Database
MOCK_SESSIONS = {
    "sess-1": {
        "id": "sess-1",
        "process_id": "proc-1",
        "status": "active",
        "start_time": "2023-10-25T10:00:00Z",
        "end_time": None
    },
    "sess-2": {
        "id": "sess-2",
        "process_id": "proc-2",
        "status": "closed",
        "start_time": "2023-10-24T09:00:00Z",
        "end_time": "2023-10-24T11:00:00Z"
    }
}


@DebugSessionAPI.read(leaf="")
def list_sessions(process_id: str = None, status: str = None) -> Dict[str, Any]:
    """List debug sessions"""
    filtered_sessions = list(MOCK_SESSIONS.values())
    if process_id:
        filtered_sessions = [s for s in filtered_sessions if s['process_id'] == process_id]
    if status:
        filtered_sessions = [s for s in filtered_sessions if s['status'] == status]

    return {
        'total': len(filtered_sessions),
        'sessions': filtered_sessions
    }

@DebugSessionAPI.create(leaf="")
def create_session(body: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new debug session"""
    if not body or 'process_id' not in body:
        raise ValueError("Missing process_id")

    new_id = f"sess-{len(MOCK_SESSIONS) + 1}"
    MOCK_SESSIONS[new_id] = {
        "id": new_id,
        "process_id": body['process_id'],
        "status": "active",
        "start_time": "2023-10-25T12:00:00Z",
        "end_time": None
    }
    return {"id": new_id, "message": "Session created successfully"}

@DebugSessionAPI.read(leaf="/{id}")
def get_session(id: str) -> Dict[str, Any]:
    """Get session detail"""
    if id not in MOCK_SESSIONS:
        raise ValueError("Session not found")
    return MOCK_SESSIONS[id]

@DebugSessionAPI.create(leaf="/{id}/close")
def close_session(id: str) -> Dict[str, Any]:
    """Close a debug session"""
    if id not in MOCK_SESSIONS:
        raise ValueError("Session not found")

    if MOCK_SESSIONS[id]['status'] == 'closed':
        return {"message": "Session is already closed"}

    MOCK_SESSIONS[id]['status'] = 'closed'
    MOCK_SESSIONS[id]['end_time'] = "2023-10-25T13:00:00Z" # Mock time
    return {"message": "Session closed successfully"}
