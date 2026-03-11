# S6.6 — Timeline Viewer: Requirements

## Overview
Interactive, zoomable timeline visualization of trace events within a session, anchored to gateway start.

## Requirements (EARS Notation)

### REQ-S6.6-001: Timeline Display
The view shall render trace events on a horizontal timeline anchored to the gateway start timestamp.

### REQ-S6.6-002: Zoom and Pan
The view shall support zooming in/out and panning the timeline.

### REQ-S6.6-003: Event Filtering
The view shall support filtering events by portal scope and event type.

### REQ-S6.6-004: Event Inspection
WHEN a user clicks an event on the timeline, THE view SHALL display an event detail panel with all event fields.

### REQ-S6.6-005: Color Coding
Different event types shall be displayed with distinct colors.

## Acceptance Criteria
- Timeline renders events in chronological order.
- Zoom/pan provides detailed and overview perspectives.
- Clicking an event shows its details.
