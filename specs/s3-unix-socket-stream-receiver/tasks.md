# S3.2 — Unix Socket Stream Receiver: Tasks

## Implementation Tasks

- [ ] Create `streamreceiver/unix_receiver.py` with `UnixSocketStreamReceiver`
- [ ] Implement socket file cleanup on start and stop
- [ ] Reuse handshake/auth logic from TCP receiver (extract common base)
- [ ] Implement `start()` and `stop()` methods

## Testing Tasks

- [ ] Test listener accepts connections on configured Unix socket path
- [ ] Test stale socket file is removed on start
- [ ] Test socket file is removed on stop
- [ ] Test authentication and data forwarding work identically to TCP
