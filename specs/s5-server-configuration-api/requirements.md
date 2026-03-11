# S5.7 — Server Configuration API: Requirements

## Overview
Endpoints to view and modify server configuration (listen addresses, retention policies, connection limits). Restricted to administrative users.

## Requirements (EARS Notation)

### REQ-S5.7-001: Get Configuration
The system shall expose `GET /api/v1/config` returning all configuration key-value pairs.

### REQ-S5.7-002: Update Configuration
The system shall expose `PUT /api/v1/config/{key}` accepting a new value for a configuration key.

### REQ-S5.7-003: Validation
WHEN a configuration update is submitted, THE system SHALL validate the value type and constraints before persisting.

### REQ-S5.7-004: Admin Only
All server configuration endpoints shall require the `admin` role (S7.3).

## Acceptance Criteria
- All configuration values can be read and updated.
- Invalid values are rejected with descriptive errors.
- Non-admin users receive 403.
