# S4.6 — Search and Query Engine: Tasks

## Implementation Tasks

- [ ] Create `tracedata/search.py` with `SearchQuery`, `SearchResult`, `TraceSearchEngine`
- [ ] Implement multi-criteria filter chain
- [ ] Implement text search (partial match) on string fields
- [ ] Implement portal scope filtering integration
- [ ] Implement result ordering and pagination

## Testing Tasks

- [ ] Test single-criterion filtering (by filename, function, line, event_type)
- [ ] Test multi-criteria combination
- [ ] Test partial text search matching
- [ ] Test pagination offset and limit
- [ ] Test total_count is correct regardless of pagination
- [ ] Test ordering ascending and descending
