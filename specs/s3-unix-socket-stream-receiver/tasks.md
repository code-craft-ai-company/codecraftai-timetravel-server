# S3.2 — Unix Socket Stream Receiver: Tasks

## Implementation Tasks

- [x] Create `streamreceiver/unix_receiver.py` with `UnixSocketStreamReceiver`
- [x] Implement socket file cleanup on start and stop
- [x] Reuse handshake/auth logic from TCP receiver (extract common base)
- [x] Implement `start()` and `stop()` methods

## Testing Tasks

- [x] Test listener accepts connections on configured Unix socket path
- [x] Test stale socket file is removed on start
- [x] Test socket file is removed on stop
- [x] Test authentication and data forwarding work identically to TCP
