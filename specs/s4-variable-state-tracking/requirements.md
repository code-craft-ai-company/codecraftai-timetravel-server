# S4.5 — Variable State Tracking: Requirements

## Overview
Aggregates `VariableSnapshotEvent` data to produce per-variable value histories across time, enabling variable-value inspection at any point in the trace.

## Requirements (EARS Notation)

### REQ-S4.5-001: Variable History
WHEN `VariableSnapshotEvent` events exist, THE system SHALL aggregate them into a per-variable history showing each value and its timestamp offset.

### REQ-S4.5-002: Point-in-Time Query
WHEN a timestamp offset is provided, THE system SHALL return the value of a specified variable at that point in time (most recent snapshot before the timestamp).

### REQ-S4.5-003: Variable Listing
The system shall provide a list of all variable names that have snapshots within a given scope (timeline, portal, file).

### REQ-S4.5-004: Value Changes
The system shall identify points where a variable's value changed and provide a diff-like view of the changes.

## Acceptance Criteria
- Variable history is correctly aggregated from snapshot events.
- Point-in-time query returns the correct value.
- Variable listing shows all captured variables.
