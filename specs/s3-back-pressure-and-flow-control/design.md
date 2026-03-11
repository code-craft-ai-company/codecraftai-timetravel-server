# S3.5 — Back-Pressure and Flow Control: Design

## Technical Architecture

### Module Layout
```
source/packages/automojo/timetravelserver/
    streamreceiver/
        flow_control.py   # FlowController
```

### Class: FlowController

```python
class FlowController:
    def __init__(self, high_watermark: int = 1_048_576, low_watermark: int = 524_288,
                 global_limit: int = 104_857_600):
        ...

    def register_connection(self, conn_id: str) -> None:
    def unregister_connection(self, conn_id: str) -> None:
    def report_buffer_size(self, conn_id: str, size: int) -> FlowAction:
    def should_accept_new(self) -> bool:
```

### FlowAction Enum
```python
class FlowAction:
    CONTINUE = "continue"
    PAUSE = "pause"
    RESUME = "resume"
```

### Integration
- Called by `StreamSessionLifecycle` after each read chunk.
- When `PAUSE` is returned, the session stops reading from the socket.
- When buffer is consumed and drops to low watermark, session calls again and gets `RESUME`.

### Dependencies
- Standalone; used by S3.4 (StreamSessionLifecycle).
