# S1.1 — Service Registration Endpoint: Requirements

## Overview
Receives registration requests from pod remote-control instances (pod F5.3). Validates the instance credential, records process metadata, and assigns a server-side process identifier.

## User Stories

### US-1: Pod Registration
As a pod remote-control instance, I want to register with the server so that operators can see and control my process.

### US-2: Credential Validation on Registration
As a server operator, I want registration requests validated against stored credentials so that only authorized processes can register.

## Requirements (EARS Notation)

### REQ-S1.1-001: Registration Endpoint
The system shall expose an HTTP POST endpoint that accepts registration requests containing: `credential_token`, `host`, `pid`, `application_name`, `pod_version`, and `remote_control_address`.

### REQ-S1.1-002: Credential Validation
WHEN a registration request is received, THE system SHALL validate the `credential_token` against the credential store (S0.2) before processing the registration.

### REQ-S1.1-003: Invalid Credential Rejection
IF the credential token is invalid, revoked, or expired, THEN THE system SHALL reject the registration with HTTP 401 Unauthorized.

### REQ-S1.1-004: Process Record Creation
WHEN credentials are valid, THE system SHALL create a `RegisteredProcess` record with lifecycle state `registered` and return the assigned process `id`.

### REQ-S1.1-005: Duplicate Registration Handling
WHEN a registration request matches an existing process with the same `host` and `pid`, THE system SHALL update the existing record rather than creating a duplicate.

### REQ-S1.1-006: Response Format
The system shall return a JSON response with `process_id` (UUID) and `status` ("registered") on success.

## Acceptance Criteria
- A pod with valid credentials can register and receive a process ID.
- A pod with invalid credentials receives 401.
- Duplicate host+pid registration updates the existing record.
- The registered process appears in the process registry (S1.4).
