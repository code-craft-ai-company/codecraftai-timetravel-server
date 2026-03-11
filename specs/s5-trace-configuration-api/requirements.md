# S5.3 — Trace Configuration API: Requirements

## Overview
Endpoints to get and update the trace configuration on a target process (granularity, inner-portal annotations).

## Requirements (EARS Notation)

### REQ-S5.3-001: Get Configuration
The system shall expose `GET /api/v1/processes/{id}/trace-config` returning the current trace configuration.

### REQ-S5.3-002: Update Configuration
The system shall expose `PUT /api/v1/processes/{id}/trace-config` accepting `granularity` and `record_inner_portals` fields.

### REQ-S5.3-003: Authentication
All endpoints shall require API authentication (S7.2).

## Acceptance Criteria
- GET returns current configuration from the remote process.
- PUT updates configuration and returns the confirmed result.
