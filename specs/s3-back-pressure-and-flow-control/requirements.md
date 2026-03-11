# S3.5 — Back-Pressure and Flow Control: Requirements

## Overview
Monitors ingestion rate and storage throughput. Applies back-pressure to incoming streams when the server is saturated, preventing memory exhaustion and data loss.

## User Stories

### US-1: Overload Protection
As the server, I need to apply back-pressure to data senders when I cannot keep up so that memory is not exhausted.

## Requirements (EARS Notation)

### REQ-S3.5-001: Buffer Monitoring
WHILE streams are active, THE system SHALL monitor the size of in-memory receive buffers per connection.

### REQ-S3.5-002: High Watermark
WHEN the receive buffer exceeds a configurable high watermark, THE system SHALL pause reading from the socket to apply TCP back-pressure.

### REQ-S3.5-003: Low Watermark
WHEN the receive buffer drops below a configurable low watermark, THE system SHALL resume reading from the socket.

### REQ-S3.5-004: Global Memory Limit
WHEN the total memory consumed by all active stream buffers exceeds a global limit, THE system SHALL reject new connections and pause reading on all active connections.

### REQ-S3.5-005: Storage Throughput
IF the storage backend write latency exceeds a threshold, THEN THE system SHALL reduce read rates to match storage throughput.

## Acceptance Criteria
- Back-pressure pauses reading when high watermark is exceeded.
- Reading resumes when buffer drops below low watermark.
- New connections are rejected when global memory limit is reached.
