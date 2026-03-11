# S2.2 — Portal Activation / Deactivation: Requirements

## Overview
Issues activate/deactivate commands to a registered process's remote-control server, targeting individual portals or bulk sets.

## User Stories

### US-1: Portal Control
As a user, I want to activate or deactivate specific portals on a remote process so that I can control what gets traced.

### US-2: Bulk Operations
As a user, I want to activate or deactivate multiple portals at once so that I can efficiently configure tracing.

## Requirements (EARS Notation)

### REQ-S2.2-001: Single Portal Activation
WHEN a user requests activation of a named portal on a process, THE system SHALL send an `activate_portal` command to the pod's remote-control server.

### REQ-S2.2-002: Single Portal Deactivation
WHEN a user requests deactivation of a named portal on a process, THE system SHALL send a `deactivate_portal` command to the pod's remote-control server.

### REQ-S2.2-003: Bulk Operations
The system shall support activating or deactivating a list of portal names in a single operation.

### REQ-S2.2-004: State Confirmation
WHEN a portal command succeeds, THE system SHALL update the local `portal_snapshots` to reflect the new activation state.

### REQ-S2.2-005: Error Propagation
IF a portal command fails on the remote, THEN THE system SHALL propagate the error message to the caller.

## Acceptance Criteria
- Single portal activate/deactivate commands are sent and confirmed.
- Bulk operations process all portals in the list.
- Local portal snapshots reflect the updated state.
- Errors from the remote are propagated.
