# S5.8 — Server Health API: Design

## Endpoints

| Method | Path | Auth | Response |
|---|---|---|---|
| GET | `/api/v1/health` | None | Health status JSON |

### Response Format
```json
{
    "status": "healthy",
    "uptime_seconds": 86400,
    "active_connections": 5,
    "registered_process_count": 12,
    "active_session_count": 3,
    "storage_utilization_bytes": 1048576,
    "components": {
        "database": "ok",
        "stream_receiver": "ok",
        "storage_backend": "ok"
    }
}
```

### Module: `health.py` in REST API v1 feature directory.

### Dependencies
- S0.3 (ServerConfigStore), S1.4 (ProcessRegistry), S2.4 (DebugSessionManager)
