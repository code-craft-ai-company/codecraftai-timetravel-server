# S1.5 — Process Metadata Refresh: Requirements

## Overview
Mechanism to re-query a registered process's remote-control interface (pod F5.1) to refresh portal lists, trace configuration, and connection status on demand.

## User Stories

### US-1: On-Demand Refresh
As an operator, I want to refresh a process's metadata on demand so that I see the latest portal state without waiting for the next heartbeat.

## Requirements (EARS Notation)

### REQ-S1.5-001: Refresh Command
The system shall provide a method to trigger a metadata refresh for a registered process identified by `process_id`.

### REQ-S1.5-002: Remote Query
WHEN a refresh is triggered, THE system SHALL connect to the process's `remote_control_address` and query its current portal list and trace configuration via the JSON-lines protocol (S2.5).

### REQ-S1.5-003: Data Update
WHEN remote query results are received, THE system SHALL update the process's portal snapshots and trace configuration in the database.

### REQ-S1.5-004: Connection Failure
IF the remote query fails (connection refused, timeout), THEN THE system SHALL log the error and return a failure status without changing the process lifecycle state.

### REQ-S1.5-005: Refresh Status
The system shall return the result of the refresh operation (success with updated data, or failure with error message).

## Acceptance Criteria
- Refresh retrieves current portal list from the pod.
- Portal snapshots are updated in the database.
- Connection failures return a descriptive error.
- Process lifecycle state is not changed by a failed refresh.
