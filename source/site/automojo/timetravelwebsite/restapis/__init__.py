import os

from flask import Blueprint

def register_rest_blueprints(app, prefix):

    bp = Blueprint(prefix, __name__, url_prefix="/%s" % prefix)

    from automojo.timetravelwebsite.restapis.versions.v1 import apply_namespaces as apply_namespaces_v1
    apply_namespaces_v1(bp)

    app.register_blueprint(bp)

    return
