# S2.3 — Trace Configuration Query and Update: Design

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    debugcontrol/
        trace_config.py   # TraceConfigService
```

### Class: TraceConfigService

```python
class TraceConfigService:
    def __init__(self, session_factory, command_dispatcher: CommandDispatcher):
        ...

    def get_config(self, process_id: UUID) -> TraceConfigInfo:
        """Query pod for current trace configuration."""

    def update_config(self, process_id: UUID, granularity: Optional[str] = None,
                      record_inner_portals: Optional[bool] = None) -> TraceConfigInfo:
        """Update trace configuration on the pod."""
```

### Data Model
```python
@dataclass
class TraceConfigInfo:
    granularity: str          # "call_return", "line_level", "variable_snapshot"
    record_inner_portals: bool
```

### Dependencies
- S1.4 (ProcessRegistry)
- S2.5 (CommandDispatcher)
