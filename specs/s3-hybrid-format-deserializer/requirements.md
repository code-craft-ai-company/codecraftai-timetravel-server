# S3.3 — Hybrid Format Deserializer: Requirements

## Overview
Parses the hybrid serialization format (pod F1.3) from incoming streams — reading `struct` envelopes and `pickle` payloads — and materializes them into server-side trace event data model (S0.5).

## User Stories

### US-1: Stream Deserialization
As the server, I need to parse binary trace data from pods into structured events so that trace data can be stored, queried, and displayed.

## Requirements (EARS Notation)

### REQ-S3.3-001: Envelope Parsing
The system shall read fixed-size `struct` envelopes containing: event type (uint8), timestamp offset (float64), thread ID (uint64), filename length (uint16), line number (uint32), and payload length (uint32).

### REQ-S3.3-002: Payload Deserialization
WHEN an envelope is parsed, THE system SHALL read `payload_length` bytes and deserialize them using `pickle` protocol 5.

### REQ-S3.3-003: Event Materialization
WHEN envelope and payload are parsed, THE system SHALL construct the appropriate `TraceEvent` subclass (S0.5) with all fields populated.

### REQ-S3.3-004: Stream Processing
The system shall process a continuous byte stream, yielding events incrementally as they become available.

### REQ-S3.3-005: Corruption Handling
IF the byte stream contains corrupted data (invalid envelope size, unpickling errors), THEN THE system SHALL log the error, skip the corrupted segment, and attempt to resume parsing.

### REQ-S3.3-006: Security
The system shall use `pickle` restricted mode or validate the source before unpickling to mitigate arbitrary code execution risks.

## Acceptance Criteria
- Valid binary streams are deserialized into correct event objects.
- The deserializer yields events incrementally.
- Corrupted data is handled without crashing the receiver.
