from flask import request
from flask_restx import Namespace, Resource, fields

TRACE_DATA_NAMESPACE_PATH = "/trace-data"
trace_data_ns = Namespace("Trace Data v1", description="Trace Data API")

event_model = trace_data_ns.model('TraceEvent', {
    'id': fields.String(description='Event ID'),
    'timestamp': fields.String(description='Event timestamp (ISO 8601)'),
    'type': fields.String(description='Event type (call, return, exception)'),
    'function_name': fields.String(description='Function name'),
    'filename': fields.String(description='Source filename'),
    'line_no': fields.Integer(description='Line number')
})

event_list_model = trace_data_ns.model('TraceEventList', {
    'total': fields.Integer(description='Total number of events'),
    'events': fields.List(fields.Nested(event_model))
})

call_node_model = trace_data_ns.model('CallNode', {
    'id': fields.String(description='Node ID'),
    'function_name': fields.String(description='Function name'),
    'duration_ms': fields.Float(description='Duration in milliseconds'),
    'children': fields.List(fields.Raw, description='Child nodes') # Simplified for now
})

variable_snapshot_model = trace_data_ns.model('VariableSnapshot', {
    'timestamp': fields.String(description='Snapshot timestamp (ISO 8601)'),
    'value': fields.String(description='Variable value (string representation)'),
    'type': fields.String(description='Variable type')
})

variable_history_model = trace_data_ns.model('VariableHistory', {
    'name': fields.String(description='Variable name'),
    'history': fields.List(fields.Nested(variable_snapshot_model))
})


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


def require_auth(func):
    """Mock authentication decorator"""
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            trace_data_ns.abort(401, "Unauthorized")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


@trace_data_ns.route("/events")
class TraceEventsList(Resource):
    @trace_data_ns.doc(security='Bearer Auth')
    @require_auth
    @trace_data_ns.param('session_id', 'Filter by session ID')
    @trace_data_ns.param('type', 'Filter by event type')
    @trace_data_ns.param('function_name', 'Filter by function name')
    @trace_data_ns.param('page', 'Page number', type=int, default=1)
    @trace_data_ns.param('per_page', 'Items per page', type=int, default=10)
    @trace_data_ns.marshal_with(event_list_model)
    def get(self):
        """Get events with multi-criteria query parameters and pagination"""
        evt_type = request.args.get('type')
        function_name = request.args.get('function_name')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        filtered_events = MOCK_EVENTS
        if evt_type:
            filtered_events = [e for e in filtered_events if e['type'] == evt_type]
        if function_name:
            filtered_events = [e for e in filtered_events if e['function_name'] == function_name]

        start = (page - 1) * per_page
        end = start + per_page
        paginated_events = filtered_events[start:end]

        return {
            'total': len(filtered_events),
            'events': paginated_events
        }, 200

@trace_data_ns.route("/timeline")
class TraceTimeline(Resource):
    @trace_data_ns.doc(security='Bearer Auth')
    @require_auth
    @trace_data_ns.param('session_id', 'Session ID (required)', required=True)
    def get(self):
        """Get timeline view"""
        # For mock, just return the events as a timeline
        return {"timeline": MOCK_EVENTS}, 200

@trace_data_ns.route("/call-graph")
class TraceCallGraph(Resource):
    @trace_data_ns.doc(security='Bearer Auth')
    @require_auth
    @trace_data_ns.param('session_id', 'Session ID (required)', required=True)
    @trace_data_ns.marshal_with(call_node_model)
    def get(self):
        """Get call-graph view"""
        return MOCK_CALL_GRAPH, 200

@trace_data_ns.route("/variables")
class TraceVariableList(Resource):
    @trace_data_ns.doc(security='Bearer Auth')
    @require_auth
    @trace_data_ns.param('session_id', 'Session ID (required)', required=True)
    def get(self):
        """Get list of available variables"""
        return {"variables": list(MOCK_VARIABLES.keys())}, 200

@trace_data_ns.route("/variables/<string:name>/history")
class TraceVariableHistory(Resource):
    @trace_data_ns.doc(security='Bearer Auth')
    @require_auth
    @trace_data_ns.param('session_id', 'Session ID (required)', required=True)
    @trace_data_ns.marshal_with(variable_history_model)
    def get(self, name):
        """Get history for a specific variable"""
        if name not in MOCK_VARIABLES:
            trace_data_ns.abort(404, "Variable not found")

        return {
            "name": name,
            "history": MOCK_VARIABLES[name]
        }, 200

def publish_namespaces(version_prefix):
    ns_list = [
        (trace_data_ns, "".join([version_prefix, TRACE_DATA_NAMESPACE_PATH]))
    ]
    return ns_list
