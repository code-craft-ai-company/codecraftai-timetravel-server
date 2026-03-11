# S5.6 — Credential Management API: Tasks

## Implementation Tasks

- [ ] Create `credentials.py` API namespace
- [ ] Implement POST create, GET list, POST rotate, POST revoke, DELETE endpoints
- [ ] Add admin role requirement

## Testing Tasks

- [ ] Test create returns plaintext token
- [ ] Test list does not expose token hashes
- [ ] Test rotate returns new token and invalidates old
- [ ] Test revoke marks credential as revoked
- [ ] Test non-admin user receives 403
