# S5.6 — Credential Management API: Tasks

## Implementation Tasks

- [x] Create `credentials.py` API namespace
- [x] Implement POST create, GET list, POST rotate, POST revoke, DELETE endpoints
- [x] Add admin role requirement

## Testing Tasks

- [x] Test create returns plaintext token
- [x] Test list does not expose token hashes
- [x] Test rotate returns new token and invalidates old
- [x] Test revoke marks credential as revoked
- [x] Test non-admin user receives 403
