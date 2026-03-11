# S6.5 — Debug Session View: Requirements

## Overview
View for an active or completed debug session showing session metadata, associated portals, and navigation to trace data views.

## Requirements (EARS Notation)

### REQ-S6.5-001: Session Metadata
The view shall display: session ID, status, process name, started_at, stopped_at (if completed), duration.

### REQ-S6.5-002: Associated Portals
The view shall list the portals included in the session.

### REQ-S6.5-003: Navigation
The view shall provide links to: Timeline Viewer (S6.6), Call Graph Viewer (S6.7), Variable Inspector (S6.8).

### REQ-S6.5-004: Close Session
IF the session is active, THE view SHALL provide a "Close Session" button.

## Acceptance Criteria
- Session metadata is displayed correctly.
- Navigation links go to the correct trace data views.
