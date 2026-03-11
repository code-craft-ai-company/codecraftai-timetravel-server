# S4.5 — Variable State Tracking: Tasks

## Implementation Tasks

- [ ] Create `tracedata/variable_tracker.py` with `VariableTracker` and `VariableChange`
- [ ] Implement `build_histories()` — aggregate VariableSnapshotEvents
- [ ] Implement `value_at()` — binary search on history
- [ ] Implement `list_variables()` — extract unique variable names
- [ ] Implement `find_changes()` — identify value change points

## Testing Tasks

- [ ] Test history aggregation groups by variable name
- [ ] Test value_at returns correct snapshot for given timestamp
- [ ] Test value_at returns None before any snapshot
- [ ] Test list_variables returns all unique names
- [ ] Test find_changes identifies value transitions
