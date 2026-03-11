# S5.4 — Debug Session API: Requirements

## Overview
Endpoints to create, list, get detail, and close debug sessions. Includes endpoints to retrieve trace data summaries and timeline metadata.

## Requirements (EARS Notation)

### REQ-S5.4-001: Create Session
The system shall expose `POST /api/v1/sessions` accepting `process_id` and `portal_names` to create a new debug session.

### REQ-S5.4-002: List Sessions
The system shall expose `GET /api/v1/sessions` with optional `process_id` and `status` query parameters.

### REQ-S5.4-003: Get Session Detail
The system shall expose `GET /api/v1/sessions/{id}` returning session metadata, portal list, and trace data summary.

### REQ-S5.4-004: Close Session
The system shall expose `POST /api/v1/sessions/{id}/close`.

### REQ-S5.4-005: Authentication
All endpoints shall require API authentication (S7.2).

## Acceptance Criteria
- Sessions can be created, listed, detailed, and closed via the API.
