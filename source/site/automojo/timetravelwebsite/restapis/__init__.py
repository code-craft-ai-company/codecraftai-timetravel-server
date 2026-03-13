import os

def register_rest_blueprints(app=None, prefix=None):
    # This hook is used by the main service to initialize REST APIs.
    # We call the v1 apply_namespaces to ensure all endpoint modules are imported
    # and registered with the automojo-webworks EndpointRegistry.
    from automojo.timetravelwebsite.restapis.versions.v1 import apply_namespaces as apply_namespaces_v1
    apply_namespaces_v1()

    return
