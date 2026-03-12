# S4.2 — Timeline Reconstruction: Tasks

## Implementation Tasks

- [x] Create `tracedata/timeline.py` with `Timeline` dataclass and `TimelineBuilder`
- [x] Implement `build()` — sort events by timestamp_offset, compute metadata
- [x] Implement `merge()` — heap-merge multiple timelines
- [x] Implement `select_range()` — filter by timestamp range

## Testing Tasks

- [x] Test build produces chronologically ordered events
- [x] Test metadata (duration, counts) is computed correctly
- [x] Test merge of two timelines produces correct order
- [x] Test select_range returns only events within range
- [x] Test empty timeline handling
