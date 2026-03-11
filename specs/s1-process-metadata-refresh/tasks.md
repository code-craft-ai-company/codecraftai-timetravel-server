# S1.5 — Process Metadata Refresh: Tasks

## Implementation Tasks

- [ ] Create `registration/metadata_refresh.py` with `MetadataRefreshService`
- [ ] Implement `refresh()` — remote query via CommandDispatcher, update portal snapshots
- [ ] Define `RefreshResult` dataclass (success/failure, updated data, error message)
- [ ] Handle connection failures gracefully

## Testing Tasks

- [ ] Test successful refresh updates portal snapshots
- [ ] Test refresh with unreachable process returns failure result
- [ ] Test refresh does not change process lifecycle state on failure
- [ ] Test refresh with unknown process_id returns appropriate error
