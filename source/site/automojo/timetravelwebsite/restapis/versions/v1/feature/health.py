from flask import request
from flask_restx import Namespace, Resource, fields

HEALTH_NAMESPACE_PATH = "/health"
health_ns = Namespace("Server Health v1", description="Server Health API")

component_status_model = health_ns.model('ComponentStatus', {
    'status': fields.String(description='Component status (up, down, degraded)'),
    'message': fields.String(description='Additional details or error message'),
    'latency_ms': fields.Float(description='Latency in milliseconds')
})

health_status_model = health_ns.model('HealthStatus', {
    'status': fields.String(description='Overall server status (healthy, degraded, down)'),
    'version': fields.String(description='Server version'),
    'uptime_seconds': fields.Integer(description='Server uptime in seconds'),
    'components': fields.Nested(health_ns.model('Components', {
        'database': fields.Nested(component_status_model),
        'stream_receiver': fields.Nested(component_status_model),
        'storage': fields.Nested(component_status_model)
    }))
})

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

@health_ns.route("")
class ServerHealth(Resource):
    @health_ns.marshal_with(health_status_model)
    def get(self):
        """Get overall server health and component status"""

        # Simple degraded check for tests
        status = "healthy"
        for comp_name, comp_status in MOCK_HEALTH_STATUS["components"].items():
            if comp_status["status"] != "up":
                status = "degraded"
                break

        MOCK_HEALTH_STATUS["status"] = status

        return MOCK_HEALTH_STATUS, 200

def publish_namespaces(version_prefix):
    ns_list = [
        (health_ns, "".join([version_prefix, HEALTH_NAMESPACE_PATH]))
    ]
    return ns_list
