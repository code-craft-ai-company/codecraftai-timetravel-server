# S8.1 — Database Migration Management: Requirements

## Overview
Schema migration tooling for safe, versioned database schema evolution across server upgrades.

## Requirements (EARS Notation)

### REQ-S8.1-001: Migration Framework
The system shall use Alembic for database schema migrations.

### REQ-S8.1-002: Auto-Generation
The system shall support auto-generating migration scripts from ORM model changes.

### REQ-S8.1-003: Upgrade/Downgrade
The system shall support `upgrade` (apply pending migrations) and `downgrade` (revert migrations) commands.

### REQ-S8.1-004: Version Tracking
The system shall track the current schema version in the database.

### REQ-S8.1-005: Startup Check
WHEN the server starts, THE system SHALL verify the database schema is at the expected version and log a warning if migrations are pending.

## Acceptance Criteria
- Migrations can be generated, applied, and reverted. Schema version is tracked. Startup warns about pending migrations.
