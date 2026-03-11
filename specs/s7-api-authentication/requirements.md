# S7.2 — API Authentication: Requirements

## Overview
Token-based or session-based authentication for REST API access. Supports both interactive (browser session cookie) and programmatic (API key / bearer token) access patterns.

## Requirements (EARS Notation)

### REQ-S7.2-001: Bearer Token
The system shall accept API requests with `Authorization: Bearer <token>` headers.

### REQ-S7.2-002: Session Cookie
The system shall accept API requests authenticated via browser session cookies (from S7.1).

### REQ-S7.2-003: API Key
The system shall support long-lived API keys for programmatic access.

### REQ-S7.2-004: Unauthenticated Rejection
IF a protected endpoint receives a request without valid authentication, THEN THE system SHALL return 401 Unauthorized.

## Acceptance Criteria
- Bearer tokens, session cookies, and API keys are all accepted for API access.
- Unauthenticated requests receive 401.
