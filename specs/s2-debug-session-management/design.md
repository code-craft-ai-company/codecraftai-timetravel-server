# S2.4 — Debug Session Management: Design

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    debugcontrol/
        session_manager.py   # DebugSessionManager
```

### Class: DebugSessionManager

```python
class DebugSessionManager:
    def __init__(self, session_factory):
        ...

    def create_session(self, process_id: UUID, portal_names: List[str]) -> TraceSession:
        """Create a new active debug session."""

    def close_session(self, session_id: UUID) -> TraceSession:
        """Close a session, set stopped_at and status=completed."""

    def list_sessions(self, process_id: Optional[UUID] = None,
                      status: Optional[str] = None) -> List[TraceSession]:
        """List sessions with optional filtering."""

    def get_session(self, session_id: UUID) -> Optional[TraceSession]:
        """Get session detail."""

    def update_data_reference(self, session_id: UUID, data_reference: str) -> None:
        """Link trace data storage reference to session."""
```

### Dependencies
- S0.1 (TraceSession model)
- S1.4 (ProcessRegistry — for process_id validation)
