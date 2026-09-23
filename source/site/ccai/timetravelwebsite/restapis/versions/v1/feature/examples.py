
from flask_restx import Namespace, Resource

EXAMPLE_NAMESPACE_PATH = "/example"

example_ns = Namespace("Example v1", description="")

@example_ns.route("/")
class ExampleCollection(Resource):

    def get(self):
        """
            Returns a paginated list of testjubs sorted from most recent to oldest
        """
        rtndata = []

        return rtndata

def publish_namespaces(version_prefix):
    ns_list = [
        (example_ns, "".join([version_prefix, EXAMPLE_NAMESPACE_PATH]))
    ]
    return ns_list

