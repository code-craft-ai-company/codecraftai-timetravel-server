# S1.2 — Service Unregistration Endpoint: Tasks

## Implementation Tasks

- [x] Add `unregister()` method to `RegistrationService`
- [x] Implement portal snapshot archival before state transition
- [x] Implement lifecycle state transition to `disconnected`
- [ ] Wire endpoint in REST API layer (deferred to S5.1)

## Testing Tasks

- [x] Test successful unregistration changes state to `disconnected`
- [x] Test portal snapshots are created during unregistration
- [x] Test unregistration with invalid credentials returns 401
- [x] Test unregistration with unknown process_id returns 404
- [x] Test `disconnected_at` is populated after unregistration
