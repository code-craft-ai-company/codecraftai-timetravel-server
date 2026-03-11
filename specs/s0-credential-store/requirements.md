# S0.2 — Credential Store: Requirements

## Overview
Secure storage for authentication tokens used to validate incoming connections from `automojo-timetravel-pod` remote-control instances (pod F5.2). Supports creation, rotation, revocation, and lookup of per-instance credentials.

## User Stories

### US-1: Credential Lifecycle
As an administrator, I want to create, rotate, and revoke credentials so that I can control which pod instances are authorized to connect.

### US-2: Credential Lookup
As the server, I need to validate incoming credentials quickly so that unauthorized connections are rejected without delay.

## Requirements (EARS Notation)

### REQ-S0.2-001: Credential Creation
WHEN an administrator requests a new credential, THE system SHALL generate a cryptographically random token, store its hash, and return the plaintext token exactly once.

### REQ-S0.2-002: Credential Lookup
WHEN the server receives a token from a pod instance, THE system SHALL hash the token and look up the matching credential record in constant time relative to the number of credentials.

### REQ-S0.2-003: Credential Revocation
WHEN an administrator revokes a credential, THE system SHALL set the `revoked_at` timestamp and THE system SHALL reject any subsequent validation attempts using that credential.

### REQ-S0.2-004: Credential Rotation
WHEN an administrator rotates a credential, THE system SHALL revoke the old credential and create a new credential, returning the new plaintext token exactly once.

### REQ-S0.2-005: Expired Credential Rejection
WHEN a credential has an `expires_at` timestamp in the past, THE system SHALL reject validation attempts using that credential.

### REQ-S0.2-006: Token Hashing
The system shall hash tokens using a one-way cryptographic hash (SHA-256 or equivalent) before storage so that plaintext tokens are never persisted.

### REQ-S0.2-007: Credential Listing
The system shall provide a method to list all credentials with their metadata (label, created_at, last_used_at, revoked_at, expires_at) without exposing token hashes.

## Acceptance Criteria
- A created credential returns a plaintext token that can be validated.
- A revoked credential is rejected on validation.
- An expired credential is rejected on validation.
- Rotation produces a new valid token and invalidates the old one.
- Plaintext tokens are never stored in the database.
