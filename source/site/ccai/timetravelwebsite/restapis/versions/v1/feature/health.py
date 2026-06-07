from typing import Dict, Any
from ccai.webworks.endpoints.restblueprint import RestBlueprint

class ServerHealthAPI(RestBlueprint):
    base_path = "/health"
    tags = ["Server Health v1"]
    version = "1.0"

# Mock health status for testing
MOCK_HEALTH_STATUS = {
    "status": "healthy",
    "version": "1.0.0",
    "uptime_seconds": 3600,
    "components": {
        "database": {"status": "up", "latency_ms": 2.5},
        "stream_receiver": {"status": "up", "latency_ms": 1.2},
        "storage": {"status": "up", "latency_ms": 5.0}
    }
}

@ServerHealthAPI.read(leaf="")
def get_health() -> Dict[str, Any]:
    """Get overall server health and component status"""
    status = "healthy"
    for comp_name, comp_status in MOCK_HEALTH_STATUS["components"].items():
        if comp_status["status"] != "up":
            status = "degraded"
            break

    MOCK_HEALTH_STATUS["status"] = status
    return MOCK_HEALTH_STATUS

def publish_namespaces(version_prefix):
    # This is kept for compatibility with the main router registration if it exists
    # but actual routing depends on how codecraftai-webworks is wired up.
    # The blueprint registers endpoints globally via the EndpointRegistry.
    pass
