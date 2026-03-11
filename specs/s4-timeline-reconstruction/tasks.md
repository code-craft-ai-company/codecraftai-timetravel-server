# S4.2 — Timeline Reconstruction: Tasks

## Implementation Tasks

- [ ] Create `tracedata/timeline.py` with `Timeline` dataclass and `TimelineBuilder`
- [ ] Implement `build()` — sort events by timestamp_offset, compute metadata
- [ ] Implement `merge()` — heap-merge multiple timelines
- [ ] Implement `select_range()` — filter by timestamp range

## Testing Tasks

- [ ] Test build produces chronologically ordered events
- [ ] Test metadata (duration, counts) is computed correctly
- [ ] Test merge of two timelines produces correct order
- [ ] Test select_range returns only events within range
- [ ] Test empty timeline handling
