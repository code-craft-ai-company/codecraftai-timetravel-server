# S4.3 — Portal-Scoped Filtering: Tasks

## Implementation Tasks

- [x] Create `tracedata/portal_filter.py` with `PortalScopeFilter`
- [x] Implement portal scope stack tracking
- [x] Implement `filter_by_portal()` — single portal filtering
- [x] Implement `filter_by_portals()` — multi-portal filtering

## Testing Tasks

- [x] Test filtering returns only events within the target portal
- [x] Test nested portal filtering
- [x] Test multi-portal filtering
- [x] Test empty portal name returns no events
- [x] Test events outside any portal are excluded
