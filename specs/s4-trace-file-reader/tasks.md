# S4.1 — Trace File Reader (Server-Side): Tasks

## Implementation Tasks

- [ ] Create `tracedata/reader.py` with `TraceFileReader`
- [ ] Implement `read_events()` — load bytes, delegate to deserializer, yield events
- [ ] Handle corrupted data recovery via deserializer skip logic

## Testing Tasks

- [ ] Test reading valid trace data produces correct events
- [ ] Test incremental reading does not load entire file into memory
- [ ] Test reading corrupted data skips bad segments
- [ ] Test reading non-existent data reference raises error
