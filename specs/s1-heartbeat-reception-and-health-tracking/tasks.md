# S1.3 — Heartbeat Reception and Health Tracking: Tasks

## Implementation Tasks

- [ ] Create `registration/heartbeat.py`
- [ ] Implement `HeartbeatService.receive()` — validate credentials, update timestamp and state
- [ ] Implement `HealthChecker` class with `check_all()` method
- [ ] Implement stale detection logic (active → stale)
- [ ] Implement unreachable detection logic (stale → unreachable)
- [ ] Implement background scheduling for health checks

## Testing Tasks

- [ ] Test heartbeat updates `last_heartbeat_at` and state to `active`
- [ ] Test heartbeat with invalid credentials returns 401
- [ ] Test heartbeat with unknown process_id returns 404
- [ ] Test `check_all()` transitions active process to stale after timeout
- [ ] Test `check_all()` transitions stale process to unreachable after 2× timeout
- [ ] Test `check_all()` does not affect processes with recent heartbeats
