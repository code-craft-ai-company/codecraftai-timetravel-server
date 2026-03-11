# S6.9 — Source Code Viewer: Requirements

## Overview
Read-only source display with line-level event annotations, highlighting lines with trace events.

## Requirements (EARS Notation)

### REQ-S6.9-001: Source Display
The view shall render source code with syntax highlighting and line numbers.

### REQ-S6.9-002: Event Annotations
Lines that have associated trace events shall be visually annotated (gutter marker, background highlight).

### REQ-S6.9-003: Event Details
WHEN a user clicks an annotated line, THE view SHALL display the trace events at that line.

### REQ-S6.9-004: Synchronized Scrolling
The view shall support synchronized scrolling with the timeline and call graph views.

## Acceptance Criteria
- Source code is displayed with syntax highlighting.
- Lines with events are visually marked.
- Click on annotated line shows event details.
