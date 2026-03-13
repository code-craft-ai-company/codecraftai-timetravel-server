from flask import request
from flask_restx import Namespace, Resource, fields

PORTALS_NAMESPACE_PATH = "/portals"
portal_control_ns = Namespace("Portal Control v1", description="Portal Control API")

portal_model = portal_control_ns.model('Portal', {
    'id': fields.String(description='Portal ID', example='portal-123'),
    'name': fields.String(description='Portal name', example='auth.login'),
    'process_id': fields.String(description='Associated Process ID', example='proc-123'),
    'is_active': fields.Boolean(description='Whether the portal is currently active collecting data')
})

portal_list_model = portal_control_ns.model('PortalList', {
    'total': fields.Integer(description='Total number of portals'),
    'portals': fields.List(fields.Nested(portal_model))
})

bulk_action_model = portal_control_ns.model('PortalBulkAction', {
    'portal_ids': fields.List(fields.String, description='List of portal IDs to affect', required=True),
    'action': fields.String(description='Action to perform (activate, deactivate)', required=True, example='activate')
})

# Mock Database
MOCK_PORTALS = {
    "portal-1": {
        "id": "portal-1",
        "name": "core.user_login",
        "process_id": "proc-1",
        "is_active": True
    },
    "portal-2": {
        "id": "portal-2",
        "name": "billing.process_payment",
        "process_id": "proc-1",
        "is_active": False
    },
    "portal-3": {
        "id": "portal-3",
        "name": "search.query",
        "process_id": "proc-2",
        "is_active": True
    }
}

def require_auth(func):
    """Mock authentication decorator"""
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            portal_control_ns.abort(401, "Unauthorized")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


@portal_control_ns.route("")
class PortalList(Resource):
    @portal_control_ns.doc(security='Bearer Auth')
    @require_auth
    @portal_control_ns.param('process_id', 'Filter by process ID')
    @portal_control_ns.marshal_with(portal_list_model)
    def get(self):
        """List available portals"""
        process_id = request.args.get('process_id')

        filtered_portals = list(MOCK_PORTALS.values())
        if process_id:
            filtered_portals = [p for p in filtered_portals if p['process_id'] == process_id]

        return {
            'total': len(filtered_portals),
            'portals': filtered_portals
        }, 200

@portal_control_ns.route("/<string:id>/activate")
class PortalActivate(Resource):
    @portal_control_ns.doc(security='Bearer Auth')
    @require_auth
    def post(self, id):
        """Activate a specific portal"""
        if id not in MOCK_PORTALS:
            portal_control_ns.abort(404, "Portal not found")

        MOCK_PORTALS[id]['is_active'] = True
        return {"message": "Portal activated successfully"}, 200

@portal_control_ns.route("/<string:id>/deactivate")
class PortalDeactivate(Resource):
    @portal_control_ns.doc(security='Bearer Auth')
    @require_auth
    def post(self, id):
        """Deactivate a specific portal"""
        if id not in MOCK_PORTALS:
            portal_control_ns.abort(404, "Portal not found")

        MOCK_PORTALS[id]['is_active'] = False
        return {"message": "Portal deactivated successfully"}, 200

@portal_control_ns.route("/bulk")
class PortalBulkAction(Resource):
    @portal_control_ns.doc(security='Bearer Auth')
    @require_auth
    @portal_control_ns.expect(bulk_action_model)
    def post(self):
        """Perform bulk activation/deactivation of portals"""
        data = request.json
        if not data or 'portal_ids' not in data or 'action' not in data:
            portal_control_ns.abort(400, "Missing required fields")

        action = data['action']
        if action not in ['activate', 'deactivate']:
            portal_control_ns.abort(400, "Invalid action, must be 'activate' or 'deactivate'")

        is_active = (action == 'activate')
        updated = 0

        for pid in data['portal_ids']:
            if pid in MOCK_PORTALS:
                MOCK_PORTALS[pid]['is_active'] = is_active
                updated += 1

        return {"message": f"Successfully updated {updated} portals"}, 200


def publish_namespaces(version_prefix):
    ns_list = [
        (portal_control_ns, "".join([version_prefix, PORTALS_NAMESPACE_PATH]))
    ]
    return ns_list
