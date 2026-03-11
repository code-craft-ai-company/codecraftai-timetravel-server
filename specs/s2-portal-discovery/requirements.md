# S2.1 — Portal Discovery: Requirements

## Overview
Queries a registered process's remote-control server (pod F5.1) to retrieve the current list of portals and their activation state.

## User Stories

### US-1: Portal Visibility
As a user, I want to see all portals defined in a remote process so that I can decide which ones to activate for debugging.

## Requirements (EARS Notation)

### REQ-S2.1-001: Portal List Retrieval
WHEN a user requests portal discovery for a process, THE system SHALL connect to the process's remote-control address and send a `list_portals` command.

### REQ-S2.1-002: Portal State
The system shall return each portal's `name` and `is_active` status as reported by the pod.

### REQ-S2.1-003: Snapshot Persistence
WHEN portal data is retrieved, THE system SHALL update the `portal_snapshots` records for that process.

### REQ-S2.1-004: Error Handling
IF the remote process is unreachable, THEN THE system SHALL return an error indicating the connection failure.

## Acceptance Criteria
- Portal list from a reachable process is returned with name and activation state.
- Portal snapshots are updated in the database after discovery.
- Unreachable processes return a descriptive error.
