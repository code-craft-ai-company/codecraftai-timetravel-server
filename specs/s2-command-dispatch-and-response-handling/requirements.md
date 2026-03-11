# S2.5 — Command Dispatch and Response Handling: Requirements

## Overview
Low-level TCP client that speaks the JSON-lines protocol (pod F5.1) to send commands and receive responses from a pod's remote-control server.

## User Stories

### US-1: Remote Command Execution
As the server, I need to send commands to pod remote-control servers and receive structured responses so that all higher-level debug control features work.

## Requirements (EARS Notation)

### REQ-S2.5-001: JSON-Lines Protocol
The system shall communicate with pod remote-control servers using the JSON-lines protocol (one JSON object per line, newline-delimited).

### REQ-S2.5-002: Command Sending
The system shall provide a method to send a command (string command name + dict parameters) to a remote address and receive the response.

### REQ-S2.5-003: Connection Management
WHEN a command is dispatched, THE system SHALL establish a TCP connection, send the command, read the response, and close the connection.

### REQ-S2.5-004: Connection Pooling
WHERE connection pooling is enabled, THE system SHALL reuse existing connections to the same remote address.

### REQ-S2.5-005: Timeout Handling
IF a response is not received within a configurable timeout, THEN THE system SHALL close the connection and raise a timeout error.

### REQ-S2.5-006: Error Responses
WHEN the pod returns an error response, THE system SHALL raise an exception containing the error message from the pod.

### REQ-S2.5-007: Authentication
WHEN connecting to a pod, THE system SHALL include the credential token in the initial handshake message.

## Acceptance Criteria
- Commands are sent and responses received via JSON-lines protocol.
- Timeout is enforced and raises an appropriate error.
- Error responses from the pod are propagated.
- Connection is properly closed after each command (or returned to pool).
