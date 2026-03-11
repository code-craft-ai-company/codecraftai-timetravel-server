# S3.2 — Unix Socket Stream Receiver: Requirements

## Overview
Listens on Unix domain sockets for connections from pod Unix socket stream backends (pod F2.3). Intended for same-host scenarios.

## User Stories

### US-1: Local Trace Reception
As the server, I need to receive trace data over Unix domain sockets for low-latency same-host collection.

## Requirements (EARS Notation)

### REQ-S3.2-001: Unix Socket Listener
The system shall listen on a configurable Unix domain socket path (`unix_socket_path` from S0.3).

### REQ-S3.2-002: Authentication
WHEN a connection is established, THE system SHALL require credential authentication in the handshake, identical to the TCP receiver (S3.1).

### REQ-S3.2-003: Data Routing
WHILE a stream is active, THE system SHALL forward received bytes to the trace data storage backend via the stream session lifecycle.

### REQ-S3.2-004: Socket Cleanup
WHEN the receiver starts, THE system SHALL remove any stale socket file at the configured path. WHEN the receiver stops, THE system SHALL remove the socket file.

## Acceptance Criteria
- Unix socket listener accepts connections on the configured path.
- Authentication and data routing work identically to TCP.
- Stale socket files are cleaned up on start.
