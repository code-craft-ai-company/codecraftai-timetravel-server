# S3.1 — TCP Stream Receiver: Design

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    streamreceiver/
        __init__.py
        tcp_receiver.py   # TcpStreamReceiver
```

### Class: TcpStreamReceiver

```python
class TcpStreamReceiver:
    def __init__(self, config_store, credential_store, storage_backend,
                 stream_router, max_connections: int = 100):
        ...

    def start(self) -> None:
        """Start listening on configured port in a background thread."""

    def stop(self) -> None:
        """Stop listener and close all active connections."""

    def _handle_connection(self, conn: socket.socket, addr: tuple) -> None:
        """Handle a single inbound connection."""
```

### Connection Handling Flow
1. Accept connection.
2. Read handshake line (JSON: `{"token": "...", "process_id": "...", "session_id": "..."}`).
3. Validate token via `CredentialStore`.
4. If invalid → send error, close.
5. If connection limit reached → send error, close.
6. Delegate to `StreamSessionLifecycle` (S3.4) for ongoing reception.
7. Route via `StreamRouter` (S3.6).

### Threading
- Main listener thread using `socketserver.ThreadingTCPServer` or `asyncio`.
- Each connection handled in its own thread (or coroutine).

### Dependencies
- S0.2 (CredentialStore)
- S0.3 (stream_receiver_port, max_concurrent_connections)
- S0.4 (TraceStorageBackend)
- S3.4 (StreamSessionLifecycle)
- S3.6 (StreamRouter)
