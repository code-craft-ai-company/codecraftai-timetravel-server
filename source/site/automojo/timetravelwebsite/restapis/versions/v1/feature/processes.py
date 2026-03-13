from flask import request
from flask_restx import Namespace, Resource, fields

PROCESSES_NAMESPACE_PATH = "/processes"
processes_ns = Namespace("Process Management v1", description="Process Management API")

process_model = processes_ns.model('Process', {
    'id': fields.String(description='Process ID', example='proc-12345'),
    'name': fields.String(description='Process name', example='my-service'),
    'state': fields.String(description='Process state', example='connected'),
    'uptime_seconds': fields.Integer(description='Process uptime in seconds', example=3600),
})

process_detail_model = processes_ns.inherit('ProcessDetail', process_model, {
    'environment': fields.Raw(description='Process environment variables'),
    'arguments': fields.List(fields.String, description='Command line arguments'),
    'metadata': fields.Raw(description='Process metadata'),
})

process_list_model = processes_ns.model('ProcessList', {
    'total': fields.Integer(description='Total number of processes'),
    'processes': fields.List(fields.Nested(process_model)),
})

registration_req_model = processes_ns.model('ProcessRegistration', {
    'name': fields.String(description='Process name', required=True),
    'environment': fields.Raw(description='Environment variables'),
    'arguments': fields.List(fields.String, description='Command line arguments'),
})

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

def require_auth(func):
    """Mock authentication decorator"""
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            processes_ns.abort(401, "Unauthorized")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper

@processes_ns.route("")
class ProcessList(Resource):
    @processes_ns.doc(security='Bearer Auth')
    @require_auth
    @processes_ns.param('state', 'Filter by state')
    @processes_ns.param('page', 'Page number', type=int, default=1)
    @processes_ns.param('per_page', 'Items per page', type=int, default=10)
    @processes_ns.marshal_with(process_list_model)
    def get(self):
        """List processes with pagination, filtering, sorting"""
        state = request.args.get('state')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        filtered_processes = list(MOCK_PROCESSES.values())
        if state:
            filtered_processes = [p for p in filtered_processes if p['state'] == state]

        start = (page - 1) * per_page
        end = start + per_page
        paginated_processes = filtered_processes[start:end]

        return {
            'total': len(filtered_processes),
            'processes': paginated_processes
        }, 200

@processes_ns.route("/<string:id>")
class ProcessDetail(Resource):
    @processes_ns.doc(security='Bearer Auth')
    @require_auth
    @processes_ns.marshal_with(process_detail_model)
    def get(self, id):
        """Get process detail"""
        if id not in MOCK_PROCESSES:
            processes_ns.abort(404, "Process not found")
        return MOCK_PROCESSES[id], 200

    @processes_ns.doc(security='Bearer Auth')
    @require_auth
    def delete(self, id):
        """Delete disconnected process"""
        if id not in MOCK_PROCESSES:
            processes_ns.abort(404, "Process not found")

        if MOCK_PROCESSES[id]['state'] != 'disconnected':
            processes_ns.abort(400, "Can only delete disconnected processes")

        del MOCK_PROCESSES[id]
        return {"message": "Process deleted successfully"}, 200

@processes_ns.route("/<string:id>/refresh")
class ProcessRefresh(Resource):
    @processes_ns.doc(security='Bearer Auth')
    @require_auth
    def post(self, id):
        """Trigger metadata refresh"""
        if id not in MOCK_PROCESSES:
            processes_ns.abort(404, "Process not found")

        return {"message": "Refresh triggered successfully"}, 200

@processes_ns.route("/<string:id>/disconnect")
class ProcessDisconnect(Resource):
    @processes_ns.doc(security='Bearer Auth')
    @require_auth
    def post(self, id):
        """Disconnect a process"""
        if id not in MOCK_PROCESSES:
            processes_ns.abort(404, "Process not found")

        MOCK_PROCESSES[id]['state'] = 'disconnected'
        return {"message": "Process disconnected successfully"}, 200

@processes_ns.route("/register")
class ProcessRegistration(Resource):
    @processes_ns.doc(security='Bearer Auth')
    @require_auth
    @processes_ns.expect(registration_req_model)
    def post(self):
        """Register a new process"""
        data = request.json
        if not data or 'name' not in data:
            processes_ns.abort(400, "Missing required fields")

        new_id = f"proc-{len(MOCK_PROCESSES) + 1}"
        MOCK_PROCESSES[new_id] = {
            "id": new_id,
            "name": data['name'],
            "state": "connected",
            "uptime_seconds": 0,
            "environment": data.get('environment', {}),
            "arguments": data.get('arguments', []),
            "metadata": {}
        }
        return {"id": new_id, "message": "Process registered successfully"}, 201

@processes_ns.route("/<string:id>/unregister")
class ProcessUnregistration(Resource):
    @processes_ns.doc(security='Bearer Auth')
    @require_auth
    def post(self, id):
        """Unregister a process"""
        if id not in MOCK_PROCESSES:
            processes_ns.abort(404, "Process not found")

        MOCK_PROCESSES[id]['state'] = 'disconnected'
        return {"message": "Process unregistered successfully"}, 200

@processes_ns.route("/<string:id>/heartbeat")
class ProcessHeartbeat(Resource):
    @processes_ns.doc(security='Bearer Auth')
    @require_auth
    def post(self, id):
        """Send heartbeat for a process"""
        if id not in MOCK_PROCESSES:
            processes_ns.abort(404, "Process not found")

        MOCK_PROCESSES[id]['state'] = 'connected'
        return {"message": "Heartbeat received"}, 200


def publish_namespaces(version_prefix):
    ns_list = [
        (processes_ns, "".join([version_prefix, PROCESSES_NAMESPACE_PATH]))
    ]
    return ns_list
