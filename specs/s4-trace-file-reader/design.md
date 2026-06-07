# S4.1 — Trace File Reader (Server-Side): Design

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    tracedata/
        reader.py   # TraceFileReader
```

### Class: TraceFileReader

```python
class TraceFileReader:
    def __init__(self, storage_backend: TraceStorageBackend):
        ...

    def read_events(self, data_reference: str, process_id: UUID,
                    session_id: UUID) -> Iterator[TraceEvent]:
        """Read stored trace data and yield deserialized events."""
```

### Implementation
- Reads bytes from `TraceStorageBackend.read()`.
- Wraps bytes in `io.BytesIO` and delegates to `HybridFormatDeserializer` (S3.3).
- Yields events incrementally via generator.

### Dependencies
- S0.4 (TraceStorageBackend)
- S0.5 (TraceEvent model)
- S3.3 (HybridFormatDeserializer)
