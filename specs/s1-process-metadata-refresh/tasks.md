# S1.5 — Process Metadata Refresh: Tasks

## Implementation Tasks

- [x] Create `registration/metadata_refresh.py` with `MetadataRefreshService`
- [x] Implement `refresh()` — remote query via CommandDispatcher, update portal snapshots
- [x] Define `RefreshResult` dataclass (success/failure, updated data, error message)
- [x] Handle connection failures gracefully

## Testing Tasks

- [x] Test successful refresh updates portal snapshots
- [x] Test refresh with unreachable process returns failure result
- [x] Test refresh does not change process lifecycle state on failure
- [x] Test refresh with unknown process_id returns appropriate error
