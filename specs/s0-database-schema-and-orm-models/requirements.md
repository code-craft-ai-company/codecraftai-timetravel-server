# S0.1 — Database Schema and ORM Models: Requirements

## Overview
Relational models for all persistent entities — users, credentials, registered processes, portal snapshots, trace sessions, and server configuration. Provides migration support for schema evolution.

## User Stories

### US-1: Database Entity Persistence
As a server operator, I want all critical server entities persisted in a relational database so that data survives restarts and can be queried efficiently.

### US-2: Schema Evolution
As a developer, I want database schema changes managed through versioned migrations so that upgrades are safe and repeatable.

## Requirements (EARS Notation)

### REQ-S0.1-001: User Table
The system shall provide a `users` table with columns for `id` (UUID primary key), `username` (unique, non-null), `password_hash` (non-null), `email`, `role` (non-null, default `viewer`), `created_at`, and `updated_at`.

### REQ-S0.1-002: Credential Table
The system shall provide a `credentials` table with columns for `id` (UUID primary key), `token_hash` (unique, non-null), `label` (non-null), `created_at`, `last_used_at`, `revoked_at`, and `expires_at`.

### REQ-S0.1-003: Registered Process Table
The system shall provide a `registered_processes` table with columns for `id` (UUID primary key), `host` (non-null), `pid` (integer, non-null), `application_name`, `pod_version`, `remote_control_address`, `lifecycle_state` (non-null, default `registered`), `registered_at`, `last_heartbeat_at`, and `disconnected_at`.

### REQ-S0.1-004: Portal Snapshot Table
The system shall provide a `portal_snapshots` table with columns for `id` (UUID primary key), `process_id` (foreign key to `registered_processes`), `portal_name` (non-null), `is_active` (boolean, non-null), and `snapshot_at`.

### REQ-S0.1-005: Trace Session Table
The system shall provide a `trace_sessions` table with columns for `id` (UUID primary key), `process_id` (foreign key to `registered_processes`), `started_at`, `stopped_at`, `status` (non-null, default `active`), and `data_reference` (path or URI to stored trace data).

### REQ-S0.1-006: Server Configuration Table
The system shall provide a `server_configuration` table with columns for `id` (UUID primary key), `key` (unique, non-null), `value` (non-null), and `updated_at`.

### REQ-S0.1-007: ORM Model Layer
The system shall provide SQLAlchemy ORM model classes corresponding to each database table, with relationships, foreign key constraints, and default value specifications.

### REQ-S0.1-008: Schema Migration Support
The system shall support schema evolution through Alembic migration scripts that can upgrade and downgrade the schema between versions.

## Acceptance Criteria
- All tables can be created via `alembic upgrade head`.
- ORM model classes can insert, query, update, and delete rows.
- Foreign key constraints are enforced by the database.
- Each table has appropriate indexes on frequently queried columns.
