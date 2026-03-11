# S7.5 — TLS / Transport Security: Requirements

## Overview
Optional TLS termination for API and stream-receiver endpoints.

## Requirements (EARS Notation)

### REQ-S7.5-001: TLS Configuration
WHERE TLS is enabled (S0.3 `tls_enabled`), THE system SHALL configure TLS on all API and stream-receiver endpoints using the configured certificate and key.

### REQ-S7.5-002: Certificate Paths
The system shall read TLS certificate and key from paths specified in server configuration (`tls_cert_path`, `tls_key_path`).

### REQ-S7.5-003: Optional
TLS SHALL be optional — the server shall function without TLS when `tls_enabled` is `false`.

## Acceptance Criteria
- Server starts with TLS when configured. Server starts without TLS when not configured. Invalid certificate paths produce a clear startup error.
