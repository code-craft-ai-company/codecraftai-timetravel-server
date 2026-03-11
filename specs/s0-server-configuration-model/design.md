# S0.3 — Server Configuration Model: Design

## Overview
A service-layer abstraction over the `ServerConfiguration` ORM model (S0.1) that provides typed access to configuration values with defaults, validation, and caching.

## Technical Architecture

### Module Layout
```
source/packages/automojo/timetravelserver/
    persistence/
        server_config_store.py    # ServerConfigStore class
```

### Configuration Schema
```python
CONFIG_SCHEMA = {
    "listen_address":            {"type": str,   "default": "0.0.0.0"},
    "listen_port":               {"type": int,   "default": 8888},
    "tls_enabled":               {"type": bool,  "default": False},
    "tls_cert_path":             {"type": str,   "default": ""},
    "tls_key_path":              {"type": str,   "default": ""},
    "max_concurrent_connections": {"type": int,   "default": 100},
    "data_retention_days":       {"type": int,   "default": 30},
    "trace_storage_backend":     {"type": str,   "default": "filesystem"},
    "trace_storage_path":        {"type": str,   "default": "./trace-data"},
    "heartbeat_timeout_seconds": {"type": int,   "default": 60},
    "stream_receiver_port":      {"type": int,   "default": 9000},
    "unix_socket_path":          {"type": str,   "default": "/tmp/timetravel.sock"},
}
```

### Class: ServerConfigStore

```python
class ServerConfigStore:
    def __init__(self, session_factory):
        ...

    def get(self, key: str) -> Any:
        """Retrieve value by key; return default if no DB override."""

    def set(self, key: str, value: Any) -> None:
        """Validate and persist a configuration value."""

    def get_all(self) -> Dict[str, Any]:
        """Return all config as a dict with defaults filled in."""

    def validate(self, key: str, value: Any) -> None:
        """Raise ValueError if key is unknown or value type mismatches."""
```

### Dependencies
- S0.1 (ServerConfiguration ORM model, session factory)
