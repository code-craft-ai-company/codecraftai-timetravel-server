# S6.10 — Credential Management View: Requirements

## Overview
Administrative page for managing instance credentials — create, rotate, revoke, and delete.

## Requirements (EARS Notation)

### REQ-S6.10-001: Credential Table
The view shall display a table of credentials with: label, created_at, last_used_at, status (active/revoked), associated process count.

### REQ-S6.10-002: Create Credential
The view shall provide a form to create a new credential with a label and optional expiration. The resulting plaintext token shall be displayed exactly once with a copy button.

### REQ-S6.10-003: Rotate/Revoke/Delete
The view shall provide action buttons per credential for rotate, revoke, and delete operations.

### REQ-S6.10-004: Admin Only
The view shall only be accessible to users with the `admin` role.

## Acceptance Criteria
- Credential table displays correct data. Create shows token once. Rotate generates new token. Revoke marks as revoked.
