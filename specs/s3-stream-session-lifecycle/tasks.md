# S3.4 — Stream Session Lifecycle: Tasks

## Implementation Tasks

- [x] Create `streamreceiver/session_lifecycle.py` with `StreamSessionLifecycle`
- [x] Implement `run()` — full lifecycle management
- [x] Implement `_receive_loop()` — chunked reading and storage append
- [x] Implement `_handle_flush()` — persist and acknowledge
- [x] Implement `_finalize()` — atomic commit of stored data
- [x] Implement abrupt disconnect handling with cleanup

## Testing Tasks

- [x] Test full lifecycle: handshake → reception → close
- [x] Test flush acknowledgement is sent after data persistence
- [x] Test abrupt disconnect cleans up resources
- [x] Test partial write retry logic
- [x] Test finalize commits data atomically
