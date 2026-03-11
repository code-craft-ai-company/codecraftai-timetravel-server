# S5.5 — Trace Data API: Requirements

## Overview
Endpoints to query trace events within a session filtered by portal scope, time range, event type, file, function, line, and variable. Returns paginated results with timeline, call-graph, and variable-history views.

## Requirements (EARS Notation)

### REQ-S5.5-001: Event Query
The system shall expose `GET /api/v1/sessions/{id}/events` with query parameters for all search criteria (S4.6).

### REQ-S5.5-002: Timeline View
The system shall expose `GET /api/v1/sessions/{id}/timeline` returning timeline metadata and events.

### REQ-S5.5-003: Call Graph View
The system shall expose `GET /api/v1/sessions/{id}/call-graph` returning the call graph structure.

### REQ-S5.5-004: Variable History View
The system shall expose `GET /api/v1/sessions/{id}/variables/{name}` returning the variable's value history.

### REQ-S5.5-005: Pagination
All list/query endpoints shall support pagination via `offset` and `limit` query parameters.

## Acceptance Criteria
- Events can be queried with all supported filters.
- Timeline, call-graph, and variable-history views return correct structures.
- Pagination works across all query endpoints.
