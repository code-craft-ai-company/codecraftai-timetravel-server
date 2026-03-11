# S2.4 — Debug Session Management: Requirements

## Overview
Creates, tracks, and closes debug sessions. A debug session represents a logical grouping of trace-control actions and resulting trace data for one or more portals on a target process.

## User Stories

### US-1: Session Creation
As a user, I want to create a debug session for a process so that trace data is organized and associated with my debugging activity.

### US-2: Session Lifecycle
As a user, I want to close a debug session when I am done so that the session is marked as complete.

## Requirements (EARS Notation)

### REQ-S2.4-001: Session Creation
WHEN a user creates a debug session, THE system SHALL create a `TraceSession` record with status `active`, associate it with the specified `process_id`, and return the session `id`.

### REQ-S2.4-002: Session Portal Association
WHEN a session is created, THE system SHALL record the list of portal names included in the session.

### REQ-S2.4-003: Session Closure
WHEN a user closes a debug session, THE system SHALL set `stopped_at` to the current timestamp and `status` to `completed`.

### REQ-S2.4-004: Session Listing
The system shall provide a method to list sessions for a process with filtering by `status` (active, completed).

### REQ-S2.4-005: Session Detail
The system shall provide a method to retrieve full session details including associated portals and trace data references.

### REQ-S2.4-006: Data Reference Association
WHEN trace data is received for a session, THE system SHALL update the session's `data_reference` to point to the stored trace data.

## Acceptance Criteria
- A debug session can be created, listed, queried, and closed.
- Session status transitions from `active` to `completed`.
- Associated portal names are recorded.
- Trace data references are linked to sessions.
