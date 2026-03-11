# S5.2 — Portal Control API: Requirements

## Overview
Endpoints to list portals for a process, activate/deactivate individual or bulk portals, and retrieve current portal state.

## Requirements (EARS Notation)

### REQ-S5.2-001: List Portals
The system shall expose `GET /api/v1/processes/{id}/portals` returning portals with their activation state.

### REQ-S5.2-002: Activate Portal
The system shall expose `POST /api/v1/processes/{id}/portals/{name}/activate`.

### REQ-S5.2-003: Deactivate Portal
The system shall expose `POST /api/v1/processes/{id}/portals/{name}/deactivate`.

### REQ-S5.2-004: Bulk Operations
The system shall expose `POST /api/v1/processes/{id}/portals/activate` and `/deactivate` accepting a JSON array of portal names.

### REQ-S5.2-005: Authentication
All endpoints shall require API authentication (S7.2).

## Acceptance Criteria
- Portal listing returns names and activation state.
- Single and bulk activate/deactivate work and update state.
