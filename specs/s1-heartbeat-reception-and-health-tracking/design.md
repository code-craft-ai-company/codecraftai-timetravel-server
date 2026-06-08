# S1.3 — Heartbeat Reception and Health Tracking: Design

## Overview
Combines an HTTP endpoint for receiving heartbeats with a background task for detecting stale/unreachable processes.

## Technical Architecture

### Heartbeat Endpoint
- **Method**: `POST`
- **Path**: `/api/v1/processes/heartbeat`
- **Request**: `{"process_id": "uuid", "credential_token": "string"}`
- **Response (200)**: `{"status": "ok"}`

### Background Health Checker

```python
class HealthChecker:
    def __init__(self, session_factory, config_store: ServerConfigStore):
        ...

    def check_all(self) -> None:
        """Scan all processes and apply state transitions."""
        timeout = self.config_store.get("heartbeat_timeout_seconds")
        now = utcnow()
        # Active → Stale: last_heartbeat_at + timeout < now
        # Stale → Unreachable: last_heartbeat_at + 2*timeout < now
```

### Module Layout
```
source/packages/ccai/timetravelserver/
    registration/
        heartbeat.py     # HeartbeatService, HealthChecker
```

### Scheduling
The `HealthChecker.check_all()` method is invoked by a background thread or scheduler (e.g., APScheduler or a simple threading.Timer loop) at `heartbeat_timeout_seconds / 2` intervals.

### Dependencies
- S0.1 (RegisteredProcess model)
- S0.2 (CredentialStore)
- S0.3 (heartbeat_timeout_seconds config)
