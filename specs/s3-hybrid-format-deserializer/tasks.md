# S3.3 — Hybrid Format Deserializer: Tasks

## Implementation Tasks

- [x] Create `streamreceiver/deserializer.py` with `HybridFormatDeserializer`
- [x] Implement envelope parsing using `struct.unpack`
- [x] Implement payload deserialization using `pickle.loads`
- [x] Implement event materialization mapping event_type to TraceEvent subclass
- [x] Implement `deserialize_stream()` as a generator yielding events
- [x] Implement corruption detection and skip/resume logic

## Testing Tasks

- [x] Test deserialization of each event type from valid binary data
- [x] Test incremental stream processing yields events as they arrive
- [x] Test corrupted envelope is detected and skipped
- [x] Test corrupted payload (unpickling error) is handled gracefully
- [x] Test round-trip: serialize with pod format, deserialize on server
