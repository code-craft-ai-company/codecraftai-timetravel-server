# S1.2 — Service Unregistration Endpoint: Requirements

## Overview
Receives unregistration requests when a pod process shuts down gracefully (pod F5.3). Marks the process record as disconnected and archives its portal state.

## User Stories

### US-1: Graceful Shutdown
As a pod process, I want to notify the server when I shut down so that operators see accurate process status.

## Requirements (EARS Notation)

### REQ-S1.2-001: Unregistration Endpoint
The system shall expose an HTTP POST endpoint that accepts unregistration requests containing: `process_id` and `credential_token`.

### REQ-S1.2-002: Credential Validation
WHEN an unregistration request is received, THE system SHALL validate the credential token before processing.

### REQ-S1.2-003: State Transition
WHEN credentials are valid and the process exists, THE system SHALL set the process `lifecycle_state` to `disconnected` and set `disconnected_at` to the current timestamp.

### REQ-S1.2-004: Portal Archival
WHEN a process is unregistered, THE system SHALL create a final `PortalSnapshot` capturing the current portal activation state before marking the process as disconnected.

### REQ-S1.2-005: Unknown Process
IF the `process_id` does not exist, THEN THE system SHALL return HTTP 404 Not Found.

## Acceptance Criteria
- A registered process can unregister and its state changes to `disconnected`.
- Portal state is archived as a snapshot before disconnection.
- Invalid credentials return 401.
- Unknown process_id returns 404.
