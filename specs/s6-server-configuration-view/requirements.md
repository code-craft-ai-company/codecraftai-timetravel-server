# S6.11 — Server Configuration View: Requirements

## Overview
Administrative page for viewing and editing server configuration parameters with validation and apply/revert controls.

## Requirements (EARS Notation)

### REQ-S6.11-001: Configuration Table
The view shall display all configuration keys with current values, defaults, and types.

### REQ-S6.11-002: Inline Editing
The view shall support inline editing of configuration values with type-appropriate input widgets.

### REQ-S6.11-003: Validation
WHEN a value is edited, THE view SHALL validate the value client-side before submission.

### REQ-S6.11-004: Apply/Revert
The view shall provide Apply and Revert buttons to submit or discard pending changes.

### REQ-S6.11-005: Admin Only
The view shall only be accessible to users with the `admin` role.

## Acceptance Criteria
- All configuration keys are displayed. Values can be edited and applied. Invalid values show validation errors.
