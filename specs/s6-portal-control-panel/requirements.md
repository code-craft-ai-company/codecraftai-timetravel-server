# S6.4 — Portal Control Panel: Requirements

## Overview
Interactive panel for bulk portal activation/deactivation, trace configuration adjustment, and one-click debug session initiation.

## Requirements (EARS Notation)

### REQ-S6.4-001: Portal List
The panel shall display all portals with checkboxes and activation state indicators.

### REQ-S6.4-002: Bulk Controls
The panel shall provide "Activate Selected" and "Deactivate Selected" buttons for bulk operations.

### REQ-S6.4-003: Select All
The panel shall provide "Select All" and "Deselect All" controls.

### REQ-S6.4-004: Start Debug Session
The panel shall provide a "Start Debug Session" button that creates a session with the currently selected (active) portals.

### REQ-S6.4-005: Inline State Update
WHEN portal activation/deactivation succeeds, THE panel SHALL update the visual state without requiring a full page refresh.

## Acceptance Criteria
- Bulk activate/deactivate works for selected portals.
- Starting a debug session creates a session and navigates to it.
- State updates are reflected visually without page reload.
