# S5.8 — Server Health API: Requirements

## Overview
Health-check and status endpoint reporting server uptime, active connections, registered process count, stream ingestion rates, and storage utilization.

## Requirements (EARS Notation)

### REQ-S5.8-001: Health Endpoint
The system shall expose `GET /api/v1/health` returning server health status.

### REQ-S5.8-002: Health Response
The response shall include: `status` ("healthy"/"degraded"/"unhealthy"), `uptime_seconds`, `active_connections`, `registered_process_count`, `active_session_count`, `storage_utilization_bytes`.

### REQ-S5.8-003: No Authentication
The health endpoint SHALL NOT require authentication so that external monitors can check the server.

### REQ-S5.8-004: Degraded Status
IF any component is experiencing errors (database unreachable, stream receiver down), THEN THE system SHALL report status as "degraded" with details.

## Acceptance Criteria
- Health endpoint returns correct metrics.
- No authentication required.
- Degraded status is reported when components have issues.
