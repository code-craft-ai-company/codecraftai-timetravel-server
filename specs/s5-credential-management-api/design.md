# S5.6 — Credential Management API: Design

## Endpoints

| Method | Path | Service |
|---|---|---|
| POST | `/api/v1/credentials` | `CredentialStore.create()` |
| GET | `/api/v1/credentials` | `CredentialStore.list_credentials()` |
| POST | `/api/v1/credentials/{id}/rotate` | `CredentialStore.rotate()` |
| POST | `/api/v1/credentials/{id}/revoke` | `CredentialStore.revoke()` |
| DELETE | `/api/v1/credentials/{id}` | `CredentialStore.delete()` |

### Module: `credentials.py` in REST API v1 feature directory.

### Dependencies
- S0.2 (CredentialStore)
- S7.3 (Role-based access — admin required)
