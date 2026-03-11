# S7.6 — Audit Logging: Requirements

## Overview
Records security-relevant events with timestamps and actor identity for compliance and troubleshooting.

## Requirements (EARS Notation)

### REQ-S7.6-001: Logged Events
The system shall log: login/logout, credential create/rotate/revoke, portal activation/deactivation, configuration changes, registration/unregistration.

### REQ-S7.6-002: Log Fields
Each audit log entry shall include: timestamp, actor (username or pod ID), action, target resource, result (success/failure).

### REQ-S7.6-003: Persistence
Audit log entries shall be persisted to the database (S0.1 AuditLog model).

### REQ-S7.6-004: Query
The system shall provide a method to query audit logs by time range, actor, and action type.

## Acceptance Criteria
- All specified events produce audit log entries. Entries contain required fields. Logs can be queried.
