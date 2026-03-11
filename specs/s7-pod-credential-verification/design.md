# S7.4 — Pod Credential Verification: Design

## Module: `auth/pod_auth.py`

### Integration Points
- S1.1 (Registration endpoint) — calls `CredentialStore.validate()`.
- S1.3 (Heartbeat) — calls `CredentialStore.validate()`.
- S3.1/S3.2 (Stream receivers) — calls `CredentialStore.validate()` in handshake.

### Dependencies
- S0.2 (CredentialStore)
