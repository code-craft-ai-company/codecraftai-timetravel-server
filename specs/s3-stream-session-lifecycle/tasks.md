# S3.4 — Stream Session Lifecycle: Tasks

## Implementation Tasks

- [ ] Create `streamreceiver/session_lifecycle.py` with `StreamSessionLifecycle`
- [ ] Implement `run()` — full lifecycle management
- [ ] Implement `_receive_loop()` — chunked reading and storage append
- [ ] Implement `_handle_flush()` — persist and acknowledge
- [ ] Implement `_finalize()` — atomic commit of stored data
- [ ] Implement abrupt disconnect handling with cleanup

## Testing Tasks

- [ ] Test full lifecycle: handshake → reception → close
- [ ] Test flush acknowledgement is sent after data persistence
- [ ] Test abrupt disconnect cleans up resources
- [ ] Test partial write retry logic
- [ ] Test finalize commits data atomically
