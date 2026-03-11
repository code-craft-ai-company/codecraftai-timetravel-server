# S5.6 — Credential Management API: Requirements

## Overview
Endpoints to create, list, rotate, revoke, and delete instance credentials. Restricted to administrative users.

## Requirements (EARS Notation)

### REQ-S5.6-001: Create Credential
The system shall expose `POST /api/v1/credentials` accepting `label` and optional `expires_at`. Returns the plaintext token exactly once.

### REQ-S5.6-002: List Credentials
The system shall expose `GET /api/v1/credentials` returning credential metadata (no token hashes).

### REQ-S5.6-003: Rotate Credential
The system shall expose `POST /api/v1/credentials/{id}/rotate` returning a new plaintext token.

### REQ-S5.6-004: Revoke Credential
The system shall expose `POST /api/v1/credentials/{id}/revoke`.

### REQ-S5.6-005: Delete Credential
The system shall expose `DELETE /api/v1/credentials/{id}`.

### REQ-S5.6-006: Admin Only
All credential management endpoints shall require the `admin` role (S7.3).

## Acceptance Criteria
- Full CRUD + rotate/revoke lifecycle works.
- Non-admin users receive 403.
- Plaintext tokens are returned only on create/rotate.
