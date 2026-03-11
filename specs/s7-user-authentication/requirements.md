# S7.1 — User Authentication: Requirements

## Overview
User login and session management for the web UI. Supports local accounts with password hashing and optional OAuth2/OIDC integration.

## Requirements (EARS Notation)

### REQ-S7.1-001: Login
The system shall provide a login page accepting username and password.

### REQ-S7.1-002: Password Hashing
The system shall hash passwords using bcrypt before storage.

### REQ-S7.1-003: Session Management
WHEN login succeeds, THE system SHALL create a session cookie with configurable expiration.

### REQ-S7.1-004: Logout
The system shall provide a logout endpoint that invalidates the session.

### REQ-S7.1-005: OAuth2/OIDC (Optional)
WHERE an external identity provider is configured, THE system SHALL support OAuth2/OIDC login flows.

## Acceptance Criteria
- Users can log in with valid credentials and receive a session. Invalid credentials are rejected. Logout invalidates the session.
