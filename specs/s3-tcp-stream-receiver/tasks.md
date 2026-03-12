# S3.1 — TCP Stream Receiver: Tasks

## Implementation Tasks

- [x] Create `streamreceiver/` package with `__init__.py`
- [x] Create `streamreceiver/tcp_receiver.py` with `TcpStreamReceiver`
- [x] Implement `start()` — bind listener socket, start accept loop in background thread
- [x] Implement `stop()` — close listener, drain active connections
- [x] Implement `_handle_connection()` — handshake, auth, delegate to stream session
- [x] Implement connection limit enforcement

## Testing Tasks

- [x] Test listener accepts connections on configured port
- [x] Test authentication handshake accepts valid credentials
- [x] Test authentication rejects invalid credentials
- [x] Test connection limit rejection
- [x] Test data forwarding to storage backend
- [x] Test graceful stop closes all connections
