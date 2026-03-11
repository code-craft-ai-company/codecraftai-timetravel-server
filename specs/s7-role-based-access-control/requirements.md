# S7.3 — Role-Based Access Control: Requirements

## Overview
Authorization model with roles (admin, operator, viewer) controlling access to features.

## Requirements (EARS Notation)

### REQ-S7.3-001: Roles
The system shall support roles: `admin`, `operator`, `viewer`.

### REQ-S7.3-002: Role Assignment
Each user account shall have one assigned role.

### REQ-S7.3-003: Access Control
- `admin`: Full access including credentials and server configuration.
- `operator`: Process management, portal control, debug sessions, trace data.
- `viewer`: Read-only access to processes, sessions, and trace data.

### REQ-S7.3-004: Enforcement
WHEN a user attempts an action above their role, THE system SHALL return 403 Forbidden.

## Acceptance Criteria
- Role-based access is enforced on all protected endpoints. Viewers cannot modify. Operators cannot access admin functions.
