# S3.4 — Stream Session Lifecycle: Design

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    streamreceiver/
        session_lifecycle.py   # StreamSessionLifecycle
```

### Class: StreamSessionLifecycle

```python
class StreamSessionLifecycle:
    def __init__(self, storage_backend: TraceStorageBackend):
        ...

    def run(self, conn: socket.socket, process_id: UUID, session_id: UUID) -> None:
        """Manage the full lifecycle of a stream connection."""

    def _receive_loop(self, conn, data_ref: str) -> None:
        """Read data in chunks and append to storage."""

    def _handle_flush(self, conn, data_ref: str) -> None:
        """Persist buffered data and send acknowledgement."""

    def _finalize(self, data_ref: str) -> None:
        """Finalize stored data (atomic commit)."""
```

### State Machine
```
HANDSHAKE → ACTIVE → CLOSING → CLOSED
                  ↘ DISCONNECTED (abrupt)
```

### Dependencies
- S0.4 (TraceStorageBackend)
