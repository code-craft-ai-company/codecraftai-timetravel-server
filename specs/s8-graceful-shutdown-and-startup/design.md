# S8.5 — Graceful Shutdown and Startup: Design

## Module: `ops/lifecycle.py`

### Class: ServerLifecycle
```python
class ServerLifecycle:
    def __init__(self, components: List[LifecycleComponent]):
        ...
    def start(self) -> None:
        """Start all components in order."""
    def stop(self, timeout: float = 30.0) -> None:
        """Stop all components in reverse order."""
```

### Signal Handling
- Register SIGTERM and SIGINT handlers that call `stop()`.

### Dependencies
- All server components that need lifecycle management.
