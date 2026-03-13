
def apply_namespaces(bp=None):
    # Import all feature modules so that their WebWorks RestBlueprint decorators run
    # and register their endpoints with the global EndpointRegistry.
    try:
        from automojo.timetravelwebsite.restapis.versions.v1.feature import health
    except ImportError as e:
        print(f"Error importing health: {e}")

    try:
        from automojo.timetravelwebsite.restapis.versions.v1.feature import processes
    except ImportError as e:
        print(f"Error importing processes: {e}")

    try:
        from automojo.timetravelwebsite.restapis.versions.v1.feature import debug_sessions
    except ImportError as e:
        print(f"Error importing debug_sessions: {e}")

    try:
        from automojo.timetravelwebsite.restapis.versions.v1.feature import portal_control
    except ImportError as e:
        print(f"Error importing portal_control: {e}")

    try:
        from automojo.timetravelwebsite.restapis.versions.v1.feature import trace_config
    except ImportError as e:
        print(f"Error importing trace_config: {e}")

    try:
        from automojo.timetravelwebsite.restapis.versions.v1.feature import trace_data
    except ImportError as e:
        print(f"Error importing trace_data: {e}")

    try:
        from automojo.timetravelwebsite.restapis.versions.v1.feature import server_config
    except ImportError as e:
        print(f"Error importing server_config: {e}")

    try:
        from automojo.timetravelwebsite.restapis.versions.v1.feature import credentials
    except ImportError as e:
        print(f"Error importing credentials: {e}")

    return
