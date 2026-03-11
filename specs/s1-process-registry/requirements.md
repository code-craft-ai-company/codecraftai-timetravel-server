# S1.4 — Process Registry: Requirements

## Overview
In-memory and persistent registry of all known processes with their current lifecycle state. Provides query APIs for listing, filtering, and retrieving process details.

## User Stories

### US-1: Process Visibility
As a server operator, I want to list all registered processes with their current state so that I have full visibility into connected applications.

### US-2: Process Filtering
As a user, I want to filter processes by lifecycle state so that I can focus on active or problematic processes.

## Requirements (EARS Notation)

### REQ-S1.4-001: Process Listing
The system shall provide a method to list all registered processes with pagination support (offset, limit).

### REQ-S1.4-002: State Filtering
The system shall support filtering the process list by `lifecycle_state` (registered, active, stale, unreachable, disconnected).

### REQ-S1.4-003: Process Detail
The system shall provide a method to retrieve full details of a single process by its `process_id`.

### REQ-S1.4-004: Search
The system shall support searching processes by `application_name` and `host` (partial match).

### REQ-S1.4-005: Sorting
The system shall support sorting the process list by `registered_at`, `last_heartbeat_at`, or `application_name`.

### REQ-S1.4-006: Process Deletion
The system shall provide a method to permanently delete a disconnected process record and its associated portal snapshots.

## Acceptance Criteria
- Listing returns all processes with correct states.
- Pagination correctly limits results and supports offset.
- State filtering returns only processes in the specified state.
- Detail retrieval returns all process fields.
- Deletion removes the process and its snapshots.
