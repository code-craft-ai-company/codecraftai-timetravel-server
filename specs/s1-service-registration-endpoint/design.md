# S1.1 — Service Registration Endpoint: Design

## Overview
An HTTP endpoint that receives pod registration, validates credentials, and creates or updates process records.

## Technical Architecture

### Endpoint
- **Method**: `POST`
- **Path**: `/api/v1/processes/register`
- **Content-Type**: `application/json`

### Request Body
```json
{
    "credential_token": "string",
    "host": "string",
    "pid": 12345,
    "application_name": "string",
    "pod_version": "string",
    "remote_control_address": "host:port"
}
```

### Response (201 Created)
```json
{
    "process_id": "uuid",
    "status": "registered"
}
```

### Processing Flow
1. Parse and validate request body.
2. Call `CredentialStore.validate(credential_token)`.
3. If invalid → return 401.
4. Query `RegisteredProcess` by (host, pid).
5. If exists → update fields, set state to `registered`.
6. If not exists → create new `RegisteredProcess`.
7. Return process_id and status.

### Module Layout
```
source/packages/automojo/timetravelserver/
    registration/
        __init__.py
        service.py     # RegistrationService class
```

### Dependencies
- S0.1 (RegisteredProcess model)
- S0.2 (CredentialStore)
- S5.1 (REST endpoint wiring — implemented later, service logic is standalone)
