# S1.4 — Process Registry: Tasks

## Implementation Tasks

- [x] Create `registration/process_registry.py` with `ProcessRegistry` class
- [x] Implement `list_processes()` with pagination, filtering, search, and sorting
- [x] Implement `get_process()` for single-process retrieval
- [x] Implement `delete_process()` with cascade deletion of snapshots
- [x] Implement `get_process_count_by_state()` for dashboard statistics

## Testing Tasks

- [x] Test listing returns all processes
- [x] Test pagination with offset and limit
- [x] Test state filtering
- [x] Test search by application_name and host
- [x] Test sorting by different fields
- [x] Test get_process returns correct process
- [x] Test get_process returns None for unknown ID
- [x] Test delete_process removes process and snapshots
- [x] Test delete_process rejects non-disconnected processes
