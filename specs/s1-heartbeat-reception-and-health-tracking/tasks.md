# S1.3 — Heartbeat Reception and Health Tracking: Tasks

## Implementation Tasks

- [x] Create `registration/heartbeat.py`
- [x] Implement `HeartbeatService.receive()` — validate credentials, update timestamp and state
- [x] Implement `HealthChecker` class with `check_all()` method
- [x] Implement stale detection logic (active → stale)
- [x] Implement unreachable detection logic (stale → unreachable)
- [x] Implement background scheduling for health checks

## Testing Tasks

- [x] Test heartbeat updates `last_heartbeat_at` and state to `active`
- [x] Test heartbeat with invalid credentials returns 401
- [x] Test heartbeat with unknown process_id returns 404
- [x] Test `check_all()` transitions active process to stale after timeout
- [x] Test `check_all()` transitions stale process to unreachable after 2× timeout
- [x] Test `check_all()` does not affect processes with recent heartbeats
