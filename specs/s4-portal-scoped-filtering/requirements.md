# S4.3 — Portal-Scoped Filtering: Requirements

## Overview
Filters reconstructed timelines to events occurring within a specific portal scope. Supports nested portal hierarchies.

## Requirements (EARS Notation)

### REQ-S4.3-001: Portal Scope Filtering
WHEN a portal name is specified, THE system SHALL return only events that occurred within that portal's enter/exit boundaries.

### REQ-S4.3-002: Nested Portal Support
WHEN portals are nested, THE system SHALL support filtering to a specific nesting level or a specific inner portal.

### REQ-S4.3-003: Portal Boundary Detection
The system shall identify portal boundaries using `PortalEnterEvent` and `PortalExitEvent` markers in the timeline.

### REQ-S4.3-004: Multiple Portal Filter
The system shall support filtering to events within any of a specified set of portal names.

## Acceptance Criteria
- Events outside a specified portal scope are excluded.
- Nested portal filtering returns correct event subsets.
- Multiple portal names filter correctly.
