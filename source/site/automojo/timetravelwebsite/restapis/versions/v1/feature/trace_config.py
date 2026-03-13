from flask import request
from flask_restx import Namespace, Resource, fields

TRACE_CONFIG_NAMESPACE_PATH = "/trace-config"
trace_config_ns = Namespace("Trace Configuration v1", description="Trace Configuration API")

trace_config_model = trace_config_ns.model('TraceConfig', {
    'process_id': fields.String(description='Associated Process ID', required=True, example='proc-123'),
    'granularity': fields.String(description='Trace granularity (call, line, exact)', required=True, example='call'),
    'max_depth': fields.Integer(description='Maximum trace depth', example=10),
    'track_variables': fields.Boolean(description='Whether to track variable changes', example=True)
})

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

def require_auth(func):
    """Mock authentication decorator"""
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            trace_config_ns.abort(401, "Unauthorized")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper

@trace_config_ns.route("/<string:process_id>")
class TraceConfigItem(Resource):
    @trace_config_ns.doc(security='Bearer Auth')
    @require_auth
    @trace_config_ns.marshal_with(trace_config_model)
    def get(self, process_id):
        """Get trace configuration for a specific process"""
        if process_id not in MOCK_TRACE_CONFIGS:
            # Return default config if not explicitly set
            return {
                "process_id": process_id,
                "granularity": "call",
                "max_depth": 5,
                "track_variables": False
            }, 200

        return MOCK_TRACE_CONFIGS[process_id], 200

    @trace_config_ns.doc(security='Bearer Auth')
    @require_auth
    @trace_config_ns.expect(trace_config_model)
    def put(self, process_id):
        """Update trace configuration for a specific process"""
        data = request.json
        if not data:
            trace_config_ns.abort(400, "Missing request body")

        if 'granularity' in data and data['granularity'] not in VALID_GRANULARITIES:
            trace_config_ns.abort(400, f"Invalid granularity. Must be one of: {', '.join(VALID_GRANULARITIES)}")

        # Initialize if not exists
        if process_id not in MOCK_TRACE_CONFIGS:
            MOCK_TRACE_CONFIGS[process_id] = {
                "process_id": process_id,
                "granularity": "call",
                "max_depth": 5,
                "track_variables": False
            }

        # Update values
        if 'granularity' in data:
            MOCK_TRACE_CONFIGS[process_id]['granularity'] = data['granularity']
        if 'max_depth' in data:
            MOCK_TRACE_CONFIGS[process_id]['max_depth'] = data['max_depth']
        if 'track_variables' in data:
            MOCK_TRACE_CONFIGS[process_id]['track_variables'] = data['track_variables']

        return {"message": "Trace configuration updated successfully"}, 200

def publish_namespaces(version_prefix):
    ns_list = [
        (trace_config_ns, "".join([version_prefix, TRACE_CONFIG_NAMESPACE_PATH]))
    ]
    return ns_list
