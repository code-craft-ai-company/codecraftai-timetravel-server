# S6.1 — Dashboard: Requirements

## Overview
Landing page showing server health, registered process count, active debug sessions, and recent activity with quick-action links.

## Requirements (EARS Notation)

### REQ-S6.1-001: Health Summary
The dashboard shall display server health status, uptime, and component statuses from the Health API (S5.8).

### REQ-S6.1-002: Process Summary
The dashboard shall display the total number of registered processes grouped by lifecycle state.

### REQ-S6.1-003: Session Summary
The dashboard shall display the count of active and recently completed debug sessions.

### REQ-S6.1-004: Recent Activity
The dashboard shall display a feed of recent events (registrations, session starts/stops, portal activations).

### REQ-S6.1-005: Quick Actions
The dashboard shall provide quick-action links to: view processes, create a debug session, manage credentials.

### REQ-S6.1-006: Auto-Refresh
The dashboard shall auto-refresh data at a configurable interval (default 30 seconds).

## Acceptance Criteria
- Dashboard loads and displays all summary data from the REST API.
- Quick-action links navigate to the correct pages.
- Data refreshes automatically.
