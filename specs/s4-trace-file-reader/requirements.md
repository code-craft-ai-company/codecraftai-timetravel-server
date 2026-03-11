# S4.1 — Trace File Reader (Server-Side): Requirements

## Overview
Reads persisted trace data from the storage backend (S0.4) and deserializes it into `TraceEvent` objects.

## Requirements (EARS Notation)

### REQ-S4.1-001: Data Loading
WHEN a data reference is provided, THE system SHALL read the stored trace data from the storage backend and return it as a sequence of `TraceEvent` objects.

### REQ-S4.1-002: Incremental Reading
The system shall support incremental reading (streaming/generator) to avoid loading entire trace files into memory.

### REQ-S4.1-003: Format Detection
The system shall detect the trace data format (hybrid binary format from pod F1.3) and select the appropriate deserializer.

### REQ-S4.1-004: Error Recovery
IF trace data contains corrupted segments, THEN THE system SHALL skip the corrupted events and continue reading remaining events.

## Acceptance Criteria
- Stored trace data can be read and deserialized into TraceEvent objects.
- Large files are read incrementally without excessive memory use.
- Corrupted data segments are skipped gracefully.
