# S0.2 — Credential Store: Tasks

## Implementation Tasks

- [ ] Create `persistence/credential_store.py` with `CredentialStore` class
- [ ] Implement `create()` — token generation with `secrets.token_urlsafe`, SHA-256 hashing, DB insert
- [ ] Implement `validate()` — hash lookup, revocation check, expiration check, `last_used_at` update
- [ ] Implement `revoke()` — set `revoked_at` timestamp
- [ ] Implement `rotate()` — revoke old + create new with same label
- [ ] Implement `list_credentials()` — return metadata without token hashes
- [ ] Implement `get()` and `delete()` methods
- [ ] Export `CredentialStore` from `persistence/__init__.py`

## Testing Tasks

- [ ] Test credential creation returns valid plaintext token
- [ ] Test validation succeeds with correct token
- [ ] Test validation fails with incorrect token
- [ ] Test validation fails after revocation
- [ ] Test validation fails after expiration
- [ ] Test rotation invalidates old token and creates valid new token
- [ ] Test listing does not expose token hashes
- [ ] Test delete permanently removes credential
