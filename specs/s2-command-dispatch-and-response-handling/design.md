# S2.5 — Command Dispatch and Response Handling: Design

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    debugcontrol/
        command_dispatcher.py   # CommandDispatcher
```

### Class: CommandDispatcher

```python
class CommandDispatcher:
    def __init__(self, credential_token: str, timeout_seconds: float = 10.0):
        ...

    def dispatch(self, remote_address: str, command: str, params: dict = None) -> dict:
        """Send a command and return the response dict."""

    def close(self) -> None:
        """Close any pooled connections."""
```

### JSON-Lines Protocol
- **Request**: `{"command": "list_portals", "params": {}, "token": "..."}\n`
- **Response**: `{"status": "ok", "data": {...}}\n` or `{"status": "error", "message": "..."}\n`

### Implementation Details
- Uses Python `socket` module for TCP connections.
- Wraps socket in `socket.makefile()` for line-based I/O.
- Sets `socket.settimeout()` for timeout enforcement.
- Parses each response line as JSON.
- Raises `CommandError` on error responses.
- Raises `CommandTimeoutError` on timeout.

### Dependencies
- Python `socket`, `json` (stdlib)
- S0.2 (credential token for authentication)
