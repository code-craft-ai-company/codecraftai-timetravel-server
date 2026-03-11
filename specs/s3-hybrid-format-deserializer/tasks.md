# S3.3 — Hybrid Format Deserializer: Tasks

## Implementation Tasks

- [ ] Create `streamreceiver/deserializer.py` with `HybridFormatDeserializer`
- [ ] Implement envelope parsing using `struct.unpack`
- [ ] Implement payload deserialization using `pickle.loads`
- [ ] Implement event materialization mapping event_type to TraceEvent subclass
- [ ] Implement `deserialize_stream()` as a generator yielding events
- [ ] Implement corruption detection and skip/resume logic

## Testing Tasks

- [ ] Test deserialization of each event type from valid binary data
- [ ] Test incremental stream processing yields events as they arrive
- [ ] Test corrupted envelope is detected and skipped
- [ ] Test corrupted payload (unpickling error) is handled gracefully
- [ ] Test round-trip: serialize with pod format, deserialize on server
