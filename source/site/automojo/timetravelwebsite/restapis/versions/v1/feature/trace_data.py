from typing import Dict, Any
from automojo.webworks.endpoints.restblueprint import RestBlueprint
from automojo.webworks.endpoints.accesspolicy import AccessPolicy

class RequireAuth(AccessPolicy):
    def check_access(self, request: Any) -> bool:
        auth_header = getattr(request, 'headers', {}).get('Authorization')
        return bool(auth_header)

class TraceDataAPI(RestBlueprint):
    base_path = "/trace-data"
    tags = ["Trace Data v1"]
    version = "1.0"
    access_policy = RequireAuth()

# Mock Database
MOCK_EVENTS = [
    {"id": "evt-1", "timestamp": "2023-10-25T10:00:00.000Z", "type": "call", "function_name": "main", "filename": "app.py", "line_no": 10},
    {"id": "evt-2", "timestamp": "2023-10-25T10:00:00.005Z", "type": "call", "function_name": "process_data", "filename": "data.py", "line_no": 20},
    {"id": "evt-3", "timestamp": "2023-10-25T10:00:00.100Z", "type": "return", "function_name": "process_data", "filename": "data.py", "line_no": 45},
    {"id": "evt-4", "timestamp": "2023-10-25T10:00:00.105Z", "type": "return", "function_name": "main", "filename": "app.py", "line_no": 15}
]

MOCK_CALL_GRAPH = {
    "id": "evt-1",
    "function_name": "main",
    "duration_ms": 105.0,
    "children": [
        {
            "id": "evt-2",
            "function_name": "process_data",
            "duration_ms": 95.0,
            "children": []
        }
    ]
}

MOCK_VARIABLES = {
    "user_count": [
        {"timestamp": "2023-10-25T10:00:00.000Z", "value": "0", "type": "int"},
        {"timestamp": "2023-10-25T10:00:00.050Z", "value": "5", "type": "int"}
    ],
    "status": [
        {"timestamp": "2023-10-25T10:00:00.000Z", "value": "'starting'", "type": "str"},
        {"timestamp": "2023-10-25T10:00:00.100Z", "value": "'running'", "type": "str"}
    ]
}


@TraceDataAPI.read(leaf="/events")
def list_trace_events(
    session_id: str = None,
    type: str = None,
    function_name: str = None,
    page: int = 1,
    per_page: int = 10
) -> Dict[str, Any]:
    """Get events with multi-criteria query parameters and pagination"""
    filtered_events = MOCK_EVENTS
    if type:
        filtered_events = [e for e in filtered_events if e['type'] == type]
    if function_name:
        filtered_events = [e for e in filtered_events if e['function_name'] == function_name]

    start = (page - 1) * per_page
    end = start + per_page
    paginated_events = filtered_events[start:end]

    return {
        'total': len(filtered_events),
        'events': paginated_events
    }

@TraceDataAPI.read(leaf="/timeline")
def get_trace_timeline(session_id: str) -> Dict[str, Any]:
    """Get timeline view"""
    if not session_id:
        raise ValueError("Missing session_id")
    # For mock, just return the events as a timeline
    return {"timeline": MOCK_EVENTS}

@TraceDataAPI.read(leaf="/call-graph")
def get_trace_call_graph(session_id: str) -> Dict[str, Any]:
    """Get call-graph view"""
    if not session_id:
        raise ValueError("Missing session_id")
    return MOCK_CALL_GRAPH

@TraceDataAPI.read(leaf="/variables")
def get_trace_variables(session_id: str) -> Dict[str, Any]:
    """Get list of available variables"""
    if not session_id:
        raise ValueError("Missing session_id")
    return {"variables": list(MOCK_VARIABLES.keys())}

@TraceDataAPI.read(leaf="/variables/{name}/history")
def get_trace_variable_history(name: str, session_id: str) -> Dict[str, Any]:
    """Get history for a specific variable"""
    if not session_id:
        raise ValueError("Missing session_id")

    if name not in MOCK_VARIABLES:
        raise ValueError("Variable not found")

    return {
        "name": name,
        "history": MOCK_VARIABLES[name]
    }
