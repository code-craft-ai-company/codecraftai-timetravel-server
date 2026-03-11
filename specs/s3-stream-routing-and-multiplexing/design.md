# S3.6 — Stream Routing and Multiplexing: Design

## Technical Architecture

### Module Layout
```
source/packages/automojo/timetravelserver/
    streamreceiver/
        stream_router.py   # StreamRouter
```

### Class: StreamRouter

```python
class StreamRouter:
    def __init__(self, storage_backend: TraceStorageBackend,
                 session_manager: DebugSessionManager):
        ...

    def route_stream(self, process_id: UUID, session_id: UUID) -> str:
        """Create/lookup storage reference for (process_id, session_id). Returns data_reference."""

    def get_data_reference(self, process_id: UUID, session_id: UUID) -> Optional[str]:
        """Look up existing data reference."""

    def finalize_route(self, process_id: UUID, session_id: UUID) -> None:
        """Finalize storage and update session data reference."""
```

### Thread Safety
- Routing table is a `dict` protected by `threading.Lock`.

### Dependencies
- S0.4 (TraceStorageBackend)
- S2.4 (DebugSessionManager)
