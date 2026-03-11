# S1.2 — Service Unregistration Endpoint: Tasks

## Implementation Tasks

- [ ] Add `unregister()` method to `RegistrationService`
- [ ] Implement portal snapshot archival before state transition
- [ ] Implement lifecycle state transition to `disconnected`
- [ ] Wire endpoint in REST API layer (deferred to S5.1)

## Testing Tasks

- [ ] Test successful unregistration changes state to `disconnected`
- [ ] Test portal snapshots are created during unregistration
- [ ] Test unregistration with invalid credentials returns 401
- [ ] Test unregistration with unknown process_id returns 404
- [ ] Test `disconnected_at` is populated after unregistration
