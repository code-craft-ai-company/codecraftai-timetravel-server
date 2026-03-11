# S0.2 — Credential Store: Design

## Overview
The credential store provides a service-layer abstraction over the `Credential` ORM model (S0.1), encapsulating token generation, hashing, validation, rotation, and revocation logic.

## Technical Architecture

### Module Layout
```
source/packages/automojo/timetravelserver/
    persistence/
        credential_store.py    # CredentialStore class
```

### Class: CredentialStore

```python
class CredentialStore:
    def __init__(self, session_factory):
        ...

    def create(self, label: str, expires_at: Optional[datetime] = None) -> Tuple[str, Credential]:
        """Generate a random token, hash it, store the credential, return (plaintext_token, credential)."""

    def validate(self, plaintext_token: str) -> Optional[Credential]:
        """Hash the token, look up the credential. Return None if not found, revoked, or expired."""

    def revoke(self, credential_id: UUID) -> Credential:
        """Set revoked_at on the credential."""

    def rotate(self, credential_id: UUID) -> Tuple[str, Credential]:
        """Revoke the old credential and create a new one with the same label."""

    def list_credentials(self) -> List[Credential]:
        """Return all credentials with metadata (no token hashes)."""

    def get(self, credential_id: UUID) -> Optional[Credential]:
        """Retrieve a single credential by ID."""

    def delete(self, credential_id: UUID) -> None:
        """Permanently remove a credential record."""
```

### Token Generation
- Use `secrets.token_urlsafe(32)` (256-bit entropy).
- Hash with `hashlib.sha256` before storage.

### Validation Logic
1. Hash the incoming plaintext token.
2. Query `credentials` table by `token_hash`.
3. If not found → reject.
4. If `revoked_at` is not None → reject.
5. If `expires_at` is not None and `expires_at < utcnow()` → reject.
6. Update `last_used_at` → accept.

### Dependencies
- S0.1 (Credential ORM model, session factory)
- Python `secrets`, `hashlib` (stdlib)

## Cross-Cutting Concerns
- All credential operations are transactional.
- `last_used_at` updates are batched to avoid write amplification under high validation rates.
