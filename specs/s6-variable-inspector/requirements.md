# S6.8 — Variable Inspector: Requirements

## Overview
Panel displaying variable snapshots at a selected point in time or across a time range, with stepping through value changes.

## Requirements (EARS Notation)

### REQ-S6.8-001: Variable List
The panel shall display all captured variables with their current value at the selected timeline position.

### REQ-S6.8-002: Value History
WHEN a variable is selected, THE panel SHALL show its full value history with timestamps.

### REQ-S6.8-003: Stepping
The panel shall provide forward/backward stepping controls to move through value changes.

### REQ-S6.8-004: Timeline Sync
WHEN the user steps through variable changes, THE panel SHALL synchronize the timeline position in the Timeline Viewer (S6.6).

## Acceptance Criteria
- Variables are listed with values at the selected timestamp.
- Stepping navigates through value changes.
- Timeline position is synchronized.
