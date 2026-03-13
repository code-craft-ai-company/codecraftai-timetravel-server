from typing import Dict, Any
from automojo.webworks.endpoints.restblueprint import RestBlueprint
from automojo.webworks.endpoints.accesspolicy import AccessPolicy

class RequireAuth(AccessPolicy):
    def check_access(self, request: Any) -> bool:
        auth_header = getattr(request, 'headers', {}).get('Authorization')
        return bool(auth_header)

class TraceConfigAPI(RestBlueprint):
    base_path = "/trace-config"
    tags = ["Trace Configuration v1"]
    version = "1.0"
    access_policy = RequireAuth()

# Mock Database
MOCK_TRACE_CONFIGS = {
    "proc-1": {
        "process_id": "proc-1",
        "granularity": "call",
        "max_depth": 5,
        "track_variables": True
    },
    "proc-2": {
        "process_id": "proc-2",
        "granularity": "line",
        "max_depth": 10,
        "track_variables": False
    }
}

VALID_GRANULARITIES = ["call", "line", "exact"]


@TraceConfigAPI.read(leaf="/{process_id}")
def get_trace_config(process_id: str) -> Dict[str, Any]:
    """Get trace configuration for a specific process"""
    if process_id not in MOCK_TRACE_CONFIGS:
        # Return default config if not explicitly set
        return {
            "process_id": process_id,
            "granularity": "call",
            "max_depth": 5,
            "track_variables": False
        }

    return MOCK_TRACE_CONFIGS[process_id]

@TraceConfigAPI.update(leaf="/{process_id}")
def update_trace_config(process_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
    """Update trace configuration for a specific process"""
    if not body:
        raise ValueError("Missing request body")

    if 'granularity' in body and body['granularity'] not in VALID_GRANULARITIES:
        raise ValueError(f"Invalid granularity. Must be one of: {', '.join(VALID_GRANULARITIES)}")

    # Initialize if not exists
    if process_id not in MOCK_TRACE_CONFIGS:
        MOCK_TRACE_CONFIGS[process_id] = {
            "process_id": process_id,
            "granularity": "call",
            "max_depth": 5,
            "track_variables": False
        }

    # Update values
    if 'granularity' in body:
        MOCK_TRACE_CONFIGS[process_id]['granularity'] = body['granularity']
    if 'max_depth' in body:
        MOCK_TRACE_CONFIGS[process_id]['max_depth'] = body['max_depth']
    if 'track_variables' in body:
        MOCK_TRACE_CONFIGS[process_id]['track_variables'] = body['track_variables']

    return {"message": "Trace configuration updated successfully"}
