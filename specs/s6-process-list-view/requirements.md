# S6.2 — Process List View: Requirements

## Overview
Paginated, filterable table of registered processes showing name, host, PID, lifecycle state, last heartbeat, and portal count.

## Requirements (EARS Notation)

### REQ-S6.2-001: Process Table
The view shall display a table with columns: Application Name, Host, PID, State, Last Heartbeat, Portal Count.

### REQ-S6.2-002: State Filtering
The view shall provide filter controls to show processes by lifecycle state.

### REQ-S6.2-003: Sorting
The view shall support sorting by any column header.

### REQ-S6.2-004: Pagination
The view shall paginate results with configurable page size and navigation controls.

### REQ-S6.2-005: Search
The view shall provide a text search field for filtering by application name or host.

### REQ-S6.2-006: Navigation
WHEN a user clicks a process row, THE view SHALL navigate to the Process Detail View (S6.3).

### REQ-S6.2-007: State Indicators
Each lifecycle state shall be displayed with a distinct color badge (green=active, yellow=stale, red=unreachable, gray=disconnected).

## Acceptance Criteria
- Table displays all process fields correctly.
- Filtering, sorting, search, and pagination work.
- Clicking a row navigates to process detail.
