# S1.3 — Heartbeat Reception and Health Tracking: Requirements

## Overview
Receives periodic heartbeat messages from registered processes (pod F5.4). Updates last-seen timestamps and transitions processes to stale or unreachable state when heartbeats are missed.

## User Stories

### US-1: Process Liveness
As a server operator, I want to see which processes are alive and responsive so that I can identify problems quickly.

## Requirements (EARS Notation)

### REQ-S1.3-001: Heartbeat Endpoint
The system shall expose an HTTP POST endpoint that accepts heartbeat messages containing: `process_id` and `credential_token`.

### REQ-S1.3-002: Timestamp Update
WHEN a valid heartbeat is received, THE system SHALL update the process `last_heartbeat_at` to the current timestamp and THE system SHALL set `lifecycle_state` to `active`.

### REQ-S1.3-003: Stale Detection
WHILE a process has `lifecycle_state` of `active`, IF no heartbeat is received within `heartbeat_timeout_seconds` (S0.3), THEN THE system SHALL transition the process to `stale`.

### REQ-S1.3-004: Unreachable Detection
WHILE a process has `lifecycle_state` of `stale`, IF no heartbeat is received within `2 × heartbeat_timeout_seconds`, THEN THE system SHALL transition the process to `unreachable`.

### REQ-S1.3-005: Background Health Check
The system shall run a periodic background task that scans all active/stale processes and applies stale/unreachable transitions.

## Acceptance Criteria
- Heartbeat updates `last_heartbeat_at` and state to `active`.
- Process transitions to `stale` after one timeout period without heartbeat.
- Process transitions to `unreachable` after two timeout periods without heartbeat.
- Background health check runs at a configurable interval.
