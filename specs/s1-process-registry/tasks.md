# S1.4 — Process Registry: Tasks

## Implementation Tasks

- [ ] Create `registration/process_registry.py` with `ProcessRegistry` class
- [ ] Implement `list_processes()` with pagination, filtering, search, and sorting
- [ ] Implement `get_process()` for single-process retrieval
- [ ] Implement `delete_process()` with cascade deletion of snapshots
- [ ] Implement `get_process_count_by_state()` for dashboard statistics

## Testing Tasks

- [ ] Test listing returns all processes
- [ ] Test pagination with offset and limit
- [ ] Test state filtering
- [ ] Test search by application_name and host
- [ ] Test sorting by different fields
- [ ] Test get_process returns correct process
- [ ] Test get_process returns None for unknown ID
- [ ] Test delete_process removes process and snapshots
- [ ] Test delete_process rejects non-disconnected processes
