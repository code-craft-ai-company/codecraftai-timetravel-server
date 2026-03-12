# S4.1 — Trace File Reader (Server-Side): Tasks

## Implementation Tasks

- [x] Create `tracedata/reader.py` with `TraceFileReader`
- [x] Implement `read_events()` — load bytes, delegate to deserializer, yield events
- [x] Handle corrupted data recovery via deserializer skip logic

## Testing Tasks

- [x] Test reading valid trace data produces correct events
- [x] Test incremental reading does not load entire file into memory
- [x] Test reading corrupted data skips bad segments
- [x] Test reading non-existent data reference raises error
