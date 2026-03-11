# S1.2 — Service Unregistration Endpoint: Design

## Overview
An HTTP endpoint that handles graceful pod shutdown notifications. Updates process lifecycle state and archives portal snapshots.

## Technical Architecture

### Endpoint
- **Method**: `POST`
- **Path**: `/api/v1/processes/unregister`

### Request Body
```json
{
    "process_id": "uuid",
    "credential_token": "string"
}
```

### Response (200 OK)
```json
{
    "process_id": "uuid",
    "status": "disconnected"
}
```

### Processing Flow
1. Validate credential token via `CredentialStore`.
2. Look up process by `process_id`.
3. If not found → 404.
4. Create `PortalSnapshot` records for current portal state.
5. Set `lifecycle_state = "disconnected"`, `disconnected_at = utcnow()`.
6. Return confirmation.

### Module Location
Logic added to `registration/service.py` as `RegistrationService.unregister()`.

### Dependencies
- S0.1 (RegisteredProcess, PortalSnapshot models)
- S0.2 (CredentialStore)
- S1.1 (RegistrationService)
