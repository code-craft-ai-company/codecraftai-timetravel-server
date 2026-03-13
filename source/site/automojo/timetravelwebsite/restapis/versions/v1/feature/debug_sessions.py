from flask import request
from flask_restx import Namespace, Resource, fields

DEBUG_SESSIONS_NAMESPACE_PATH = "/sessions"
debug_sessions_ns = Namespace("Debug Sessions v1", description="Debug Sessions API")

session_model = debug_sessions_ns.model('DebugSession', {
    'id': fields.String(description='Session ID', example='sess-12345'),
    'process_id': fields.String(description='Associated Process ID', example='proc-123'),
    'status': fields.String(description='Session status (active, closed)', example='active'),
    'start_time': fields.String(description='Start time (ISO 8601)'),
    'end_time': fields.String(description='End time (ISO 8601)', required=False)
})

session_list_model = debug_sessions_ns.model('DebugSessionList', {
    'total': fields.Integer(description='Total number of sessions'),
    'sessions': fields.List(fields.Nested(session_model))
})

session_create_model = debug_sessions_ns.model('DebugSessionCreate', {
    'process_id': fields.String(description='Process ID to debug', required=True)
})

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

def require_auth(func):
    """Mock authentication decorator"""
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            debug_sessions_ns.abort(401, "Unauthorized")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper

@debug_sessions_ns.route("")
class DebugSessionList(Resource):
    @debug_sessions_ns.doc(security='Bearer Auth')
    @require_auth
    @debug_sessions_ns.param('process_id', 'Filter by process ID')
    @debug_sessions_ns.param('status', 'Filter by status')
    @debug_sessions_ns.marshal_with(session_list_model)
    def get(self):
        """List debug sessions"""
        process_id = request.args.get('process_id')
        status = request.args.get('status')

        filtered_sessions = list(MOCK_SESSIONS.values())
        if process_id:
            filtered_sessions = [s for s in filtered_sessions if s['process_id'] == process_id]
        if status:
            filtered_sessions = [s for s in filtered_sessions if s['status'] == status]

        return {
            'total': len(filtered_sessions),
            'sessions': filtered_sessions
        }, 200

    @debug_sessions_ns.doc(security='Bearer Auth')
    @require_auth
    @debug_sessions_ns.expect(session_create_model)
    def post(self):
        """Create a new debug session"""
        data = request.json
        if not data or 'process_id' not in data:
            debug_sessions_ns.abort(400, "Missing process_id")

        new_id = f"sess-{len(MOCK_SESSIONS) + 1}"
        MOCK_SESSIONS[new_id] = {
            "id": new_id,
            "process_id": data['process_id'],
            "status": "active",
            "start_time": "2023-10-25T12:00:00Z",
            "end_time": None
        }
        return {"id": new_id, "message": "Session created successfully"}, 201

@debug_sessions_ns.route("/<string:id>")
class DebugSessionDetail(Resource):
    @debug_sessions_ns.doc(security='Bearer Auth')
    @require_auth
    @debug_sessions_ns.marshal_with(session_model)
    def get(self, id):
        """Get session detail"""
        if id not in MOCK_SESSIONS:
            debug_sessions_ns.abort(404, "Session not found")
        return MOCK_SESSIONS[id], 200

@debug_sessions_ns.route("/<string:id>/close")
class DebugSessionClose(Resource):
    @debug_sessions_ns.doc(security='Bearer Auth')
    @require_auth
    def post(self, id):
        """Close a debug session"""
        if id not in MOCK_SESSIONS:
            debug_sessions_ns.abort(404, "Session not found")

        if MOCK_SESSIONS[id]['status'] == 'closed':
            return {"message": "Session is already closed"}, 200

        MOCK_SESSIONS[id]['status'] = 'closed'
        MOCK_SESSIONS[id]['end_time'] = "2023-10-25T13:00:00Z" # Mock time
        return {"message": "Session closed successfully"}, 200

def publish_namespaces(version_prefix):
    ns_list = [
        (debug_sessions_ns, "".join([version_prefix, DEBUG_SESSIONS_NAMESPACE_PATH]))
    ]
    return ns_list
