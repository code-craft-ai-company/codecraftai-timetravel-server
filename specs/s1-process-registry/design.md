# S1.4 — Process Registry: Design

## Overview
A service class providing query and management operations over the `RegisteredProcess` model.

## Technical Architecture

### Module Layout
```
source/packages/automojo/timetravelserver/
    registration/
        process_registry.py   # ProcessRegistry class
```

### Class: ProcessRegistry

```python
class ProcessRegistry:
    def __init__(self, session_factory):
        ...

    def list_processes(self, state: Optional[str] = None, search: Optional[str] = None,
                       sort_by: str = "registered_at", offset: int = 0, limit: int = 50) -> Tuple[List[RegisteredProcess], int]:
        """Return paginated process list and total count."""

    def get_process(self, process_id: UUID) -> Optional[RegisteredProcess]:
        """Return a single process by ID."""

    def delete_process(self, process_id: UUID) -> None:
        """Delete a disconnected process and its associated snapshots."""

    def get_process_count_by_state(self) -> Dict[str, int]:
        """Return count of processes grouped by lifecycle_state."""
```

### Query Patterns
- Filtering: `WHERE lifecycle_state = :state`
- Search: `WHERE application_name ILIKE :search OR host ILIKE :search`
- Sorting: `ORDER BY :sort_by DESC`
- Pagination: `OFFSET :offset LIMIT :limit`
- Deletion: cascade delete portal_snapshots via FK or explicit delete.

### Dependencies
- S0.1 (RegisteredProcess, PortalSnapshot models)
