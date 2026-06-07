# S0.5 — Trace Event Data Model (Server-Side): Design

## Overview
Python dataclasses representing all trace event types. These mirror `codecraftai-timetravel-pod` F0.4 but add server-side indexing metadata (process_id, session_id).

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    tracedata/
        __init__.py
        events.py     # All event dataclasses
```

### Base Event

```python
@dataclass
class TraceEvent:
    event_id: uuid.UUID
    process_id: uuid.UUID
    session_id: uuid.UUID
    thread_id: int
    timestamp_offset: float  # seconds from gateway start
    event_type: str          # discriminator

    def to_dict(self) -> dict: ...

    @classmethod
    def from_dict(cls, data: dict) -> "TraceEvent": ...
```

### Derived Events

| Class | Extra Fields |
|---|---|
| `CallEvent` | `filename`, `line_number`, `function_name`, `arguments` |
| `ReturnEvent` | `filename`, `line_number`, `function_name`, `return_value` |
| `LineEvent` | `filename`, `line_number` |
| `VariableSnapshotEvent` | `filename`, `line_number`, `variable_name`, `variable_value` |
| `PortalEnterEvent` | `portal_name` |
| `PortalExitEvent` | `portal_name` |
| `GatewayStartEvent` | `absolute_start_time` |
| `GatewayStopEvent` | *(no extra fields)* |

### Event Type Discriminator
```python
class EventType:
    CALL = "call"
    RETURN = "return"
    LINE = "line"
    VARIABLE_SNAPSHOT = "variable_snapshot"
    PORTAL_ENTER = "portal_enter"
    PORTAL_EXIT = "portal_exit"
    GATEWAY_START = "gateway_start"
    GATEWAY_STOP = "gateway_stop"
```

### Conversion from Pod Events
A `from_pod_event(pod_event, process_id, session_id)` factory method will wrap pod-side events with server indexing metadata.

### Dependencies
- Python `dataclasses`, `uuid`, `datetime` (stdlib)
