# S3.2 — Unix Socket Stream Receiver: Design

## Technical Architecture

### Module Layout
```
source/packages/automojo/timetravelserver/
    streamreceiver/
        unix_receiver.py   # UnixSocketStreamReceiver
```

### Class: UnixSocketStreamReceiver

```python
class UnixSocketStreamReceiver:
    def __init__(self, config_store, credential_store, storage_backend, stream_router):
        ...

    def start(self) -> None:
        """Remove stale socket, bind, start accept loop."""

    def stop(self) -> None:
        """Stop listener, remove socket file."""
```

### Implementation
- Mirrors `TcpStreamReceiver` but uses `socket.AF_UNIX`.
- Shares handshake and connection handling logic via a common base or mixin.
- Socket file cleanup on start and stop.

### Dependencies
- Same as S3.1 but uses Unix domain socket via S0.3 `unix_socket_path`.
