# S4.3 — Portal-Scoped Filtering: Tasks

## Implementation Tasks

- [ ] Create `tracedata/portal_filter.py` with `PortalScopeFilter`
- [ ] Implement portal scope stack tracking
- [ ] Implement `filter_by_portal()` — single portal filtering
- [ ] Implement `filter_by_portals()` — multi-portal filtering

## Testing Tasks

- [ ] Test filtering returns only events within the target portal
- [ ] Test nested portal filtering
- [ ] Test multi-portal filtering
- [ ] Test empty portal name returns no events
- [ ] Test events outside any portal are excluded
