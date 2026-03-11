# S5.1 — Process Management API: Requirements

## Overview
CRUD endpoints for registered processes: list with filtering/pagination, get detail, force-refresh metadata, force-disconnect, and delete archived records.

## Requirements (EARS Notation)

### REQ-S5.1-001: List Processes
The system shall expose `GET /api/v1/processes` returning a paginated list of registered processes with optional `state`, `search`, and `sort_by` query parameters.

### REQ-S5.1-002: Get Process Detail
The system shall expose `GET /api/v1/processes/{id}` returning full process details including portal snapshots and associated sessions.

### REQ-S5.1-003: Force Refresh
The system shall expose `POST /api/v1/processes/{id}/refresh` triggering a metadata refresh (S1.5).

### REQ-S5.1-004: Force Disconnect
The system shall expose `POST /api/v1/processes/{id}/disconnect` marking the process as disconnected.

### REQ-S5.1-005: Delete Process
The system shall expose `DELETE /api/v1/processes/{id}` permanently removing a disconnected process.

### REQ-S5.1-006: Authentication
All endpoints shall require API authentication (S7.2).

## Acceptance Criteria
- All CRUD operations return correct status codes and response bodies.
- Pagination, filtering, and sorting work as documented.
- Unauthenticated requests return 401.
