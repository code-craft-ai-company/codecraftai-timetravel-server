# S3.1 — TCP Stream Receiver: Requirements

## Overview
Listens for inbound TCP connections from pod TCP socket stream backends (pod F2.2). Authenticates the connection, associates the stream with a registered process, and routes data to the trace data storage backend.

## User Stories

### US-1: Remote Trace Reception
As the server, I need to receive trace data streams over TCP from remote pod instances so that trace data is centralized for analysis.

## Requirements (EARS Notation)

### REQ-S3.1-001: TCP Listener
The system shall listen for inbound TCP connections on a configurable port (`stream_receiver_port` from S0.3).

### REQ-S3.1-002: Authentication
WHEN a TCP connection is established, THE system SHALL require the connecting pod to present a credential token in the handshake and validate it against the credential store (S0.2).

### REQ-S3.1-003: Process Association
WHEN authentication succeeds, THE system SHALL associate the stream with the registered process identified in the handshake.

### REQ-S3.1-004: Data Routing
WHILE a stream is active, THE system SHALL forward received bytes to the trace data storage backend (S0.4) via the stream session lifecycle (S3.4).

### REQ-S3.1-005: Concurrent Connections
The system shall support multiple simultaneous TCP stream connections up to `max_concurrent_connections` (S0.3).

### REQ-S3.1-006: Connection Rejection
IF the maximum concurrent connection limit is reached, THEN THE system SHALL reject new connections with an appropriate error.

## Acceptance Criteria
- TCP listener accepts connections on the configured port.
- Authenticated connections begin receiving data.
- Unauthenticated connections are rejected.
- Multiple concurrent streams are supported.
