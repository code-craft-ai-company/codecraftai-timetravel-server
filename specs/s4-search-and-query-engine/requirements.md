# S4.6 — Search and Query Engine: Requirements

## Overview
Provides filtering and search over trace events by file, function name, line number, variable name/value, time range, portal scope, and event type.

## Requirements (EARS Notation)

### REQ-S4.6-001: Multi-Criteria Filtering
The system shall support filtering events by any combination of: `filename`, `function_name`, `line_number`, `variable_name`, `event_type`, `portal_name`, `time_range` (start_offset, end_offset).

### REQ-S4.6-002: Text Search
The system shall support partial text matching (contains) on `filename`, `function_name`, and `variable_name`.

### REQ-S4.6-003: Pagination
The system shall return search results with pagination support (offset, limit, total count).

### REQ-S4.6-004: Result Ordering
The system shall support ordering results by `timestamp_offset` (ascending or descending).

### REQ-S4.6-005: Variable Value Search
WHERE variable snapshots are present, THE system SHALL support searching by variable value (exact match or string representation contains).

## Acceptance Criteria
- Multi-criteria queries return correctly filtered results.
- Text search matches partial strings.
- Pagination returns correct subsets and total count.
- Results can be ordered by timestamp.
