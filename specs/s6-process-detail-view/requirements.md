# S6.3 — Process Detail View: Requirements

## Overview
Detailed view for a single process showing metadata, connection info, portal list with activation toggle controls, trace configuration with edit capability, and associated debug sessions.

## Requirements (EARS Notation)

### REQ-S6.3-001: Process Metadata
The view shall display: application name, host, PID, pod version, lifecycle state, registered_at, last_heartbeat_at, remote_control_address.

### REQ-S6.3-002: Portal List
The view shall display the list of portals with toggle controls for activation/deactivation.

### REQ-S6.3-003: Trace Configuration
The view shall display and allow editing of trace configuration (granularity, inner-portal annotations).

### REQ-S6.3-004: Associated Sessions
The view shall list debug sessions associated with this process.

### REQ-S6.3-005: Actions
The view shall provide buttons for: Refresh Metadata, Disconnect, Delete (if disconnected).

## Acceptance Criteria
- All process metadata is displayed.
- Portal toggles send activate/deactivate commands and update state.
- Trace configuration edits are submitted and confirmed.
