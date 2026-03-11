# S3.6 — Stream Routing and Multiplexing: Requirements

## Overview
Routes incoming trace data from multiple simultaneous streams to the correct process record and debug session. Supports concurrent streams from multiple processes.

## User Stories

### US-1: Multi-Process Support
As the server, I need to route data from many concurrent streams to the correct process and session records so that trace data is accurately attributed.

## Requirements (EARS Notation)

### REQ-S3.6-001: Process Association
WHEN a stream is authenticated, THE system SHALL associate it with the correct `RegisteredProcess` based on the process_id in the handshake.

### REQ-S3.6-002: Session Association
WHEN a stream provides a session_id in the handshake, THE system SHALL associate the stream data with the corresponding `TraceSession`.

### REQ-S3.6-003: Concurrent Streams
The system shall support receiving data from multiple processes and multiple sessions simultaneously without data mixing.

### REQ-S3.6-004: Dynamic Routing
WHEN a new debug session is created (S2.4) and a pod begins streaming, THE system SHALL automatically route incoming data to the session's storage.

### REQ-S3.6-005: Routing Table
The system shall maintain an in-memory routing table mapping (process_id, session_id) tuples to their storage references.

## Acceptance Criteria
- Data from process A is stored separately from data from process B.
- Data for session X is stored separately from data for session Y.
- Concurrent streams do not interfere with each other.
