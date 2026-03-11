# S7.4 — Pod Credential Verification: Requirements

## Overview
Validates credentials presented by pod remote-control instances during registration and heartbeat.

## Requirements (EARS Notation)

### REQ-S7.4-001: Registration Verification
WHEN a pod registration request is received, THE system SHALL verify the credential token against the credential store (S0.2).

### REQ-S7.4-002: Heartbeat Verification
WHEN a pod heartbeat is received, THE system SHALL verify the credential token.

### REQ-S7.4-003: Stream Verification
WHEN a pod stream connection is established, THE system SHALL verify the handshake credential.

### REQ-S7.4-004: Rejection
IF verification fails, THEN THE system SHALL reject the request and log the failed attempt.

## Acceptance Criteria
- Valid pod credentials are accepted. Invalid/expired/revoked credentials are rejected across all pod-facing endpoints.
