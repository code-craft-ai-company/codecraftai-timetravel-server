# S0.5 — Trace Event Data Model (Server-Side): Requirements

## Overview
Server-side representations of trace events that mirror the pod models from F0.4. Includes indexing metadata (process ID, session ID, timestamps) for efficient query and retrieval.

## User Stories

### US-1: Event Representation
As the server, I need structured representations of all trace event types so that deserialized stream data can be processed uniformly.

### US-2: Queryable Metadata
As a user, I want trace events indexed by process, session, time, and type so that I can filter and search efficiently.

## Requirements (EARS Notation)

### REQ-S0.5-001: Event Types
The system shall define dataclasses for: `CallEvent`, `ReturnEvent`, `LineEvent`, `VariableSnapshotEvent`, `PortalEnterEvent`, `PortalExitEvent`, `GatewayStartEvent`, `GatewayStopEvent`.

### REQ-S0.5-002: Common Fields
Each event dataclass shall carry: `event_id` (UUID), `process_id` (UUID), `session_id` (UUID), `thread_id` (int), `timestamp_offset` (float, seconds from gateway start), `event_type` (string enum).

### REQ-S0.5-003: CallEvent Fields
The `CallEvent` shall additionally carry: `filename` (str), `line_number` (int), `function_name` (str), `arguments` (dict, optional).

### REQ-S0.5-004: ReturnEvent Fields
The `ReturnEvent` shall additionally carry: `filename` (str), `line_number` (int), `function_name` (str), `return_value` (any, optional).

### REQ-S0.5-005: LineEvent Fields
The `LineEvent` shall additionally carry: `filename` (str), `line_number` (int).

### REQ-S0.5-006: VariableSnapshotEvent Fields
The `VariableSnapshotEvent` shall additionally carry: `filename` (str), `line_number` (int), `variable_name` (str), `variable_value` (any).

### REQ-S0.5-007: Portal Events
The `PortalEnterEvent` and `PortalExitEvent` shall additionally carry: `portal_name` (str).

### REQ-S0.5-008: Gateway Events
The `GatewayStartEvent` shall carry: `absolute_start_time` (datetime). The `GatewayStopEvent` shall carry no additional fields beyond common fields.

### REQ-S0.5-009: Pod Compatibility
The server-side event dataclasses shall be structurally compatible with the pod-side event model (pod F0.4) so that deserialized pod events can be converted to server events without data loss.

## Acceptance Criteria
- All eight event types can be instantiated with their required fields.
- Common fields are present on every event type.
- Events can be serialized to and from dictionaries for API responses.
