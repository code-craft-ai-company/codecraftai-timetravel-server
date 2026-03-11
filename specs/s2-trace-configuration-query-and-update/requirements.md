# S2.3 — Trace Configuration Query and Update: Requirements

## Overview
Retrieves and modifies the trace configuration (granularity, inner-portal annotations) on a registered process via its remote-control interface.

## User Stories

### US-1: Configuration Visibility
As a user, I want to see the current trace configuration of a remote process so that I understand what is being traced.

### US-2: Configuration Control
As a user, I want to update trace granularity and annotation settings remotely so that I can tune tracing without restarting the target application.

## Requirements (EARS Notation)

### REQ-S2.3-001: Configuration Query
WHEN a user requests the trace configuration for a process, THE system SHALL send a `get_trace_config` command to the pod's remote-control server and return the result.

### REQ-S2.3-002: Configuration Update
WHEN a user submits updated trace configuration, THE system SHALL send an `update_trace_config` command to the pod's remote-control server.

### REQ-S2.3-003: Supported Settings
The system shall support querying and updating: `granularity` (call_return, line_level, variable_snapshot), `record_inner_portals` (boolean).

### REQ-S2.3-004: Update Confirmation
WHEN a configuration update succeeds, THE system SHALL return the updated configuration as confirmed by the pod.

### REQ-S2.3-005: Error Handling
IF the remote process rejects the configuration update, THEN THE system SHALL return the error message from the pod.

## Acceptance Criteria
- Current trace configuration is retrieved from a reachable process.
- Configuration updates are sent and confirmed.
- Invalid configuration values are rejected by the pod and error is returned.
