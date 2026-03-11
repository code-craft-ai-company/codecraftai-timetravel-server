# S3.1 — TCP Stream Receiver: Tasks

## Implementation Tasks

- [ ] Create `streamreceiver/` package with `__init__.py`
- [ ] Create `streamreceiver/tcp_receiver.py` with `TcpStreamReceiver`
- [ ] Implement `start()` — bind listener socket, start accept loop in background thread
- [ ] Implement `stop()` — close listener, drain active connections
- [ ] Implement `_handle_connection()` — handshake, auth, delegate to stream session
- [ ] Implement connection limit enforcement

## Testing Tasks

- [ ] Test listener accepts connections on configured port
- [ ] Test authentication handshake accepts valid credentials
- [ ] Test authentication rejects invalid credentials
- [ ] Test connection limit rejection
- [ ] Test data forwarding to storage backend
- [ ] Test graceful stop closes all connections
