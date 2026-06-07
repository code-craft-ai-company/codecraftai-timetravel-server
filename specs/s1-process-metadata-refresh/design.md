# S1.5 — Process Metadata Refresh: Design

## Overview
Combines process registry lookup with remote command dispatch to refresh portal and configuration data.

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    registration/
        metadata_refresh.py   # MetadataRefreshService
```

### Class: MetadataRefreshService

```python
class MetadataRefreshService:
    def __init__(self, session_factory, command_dispatcher: CommandDispatcher):
        ...

    def refresh(self, process_id: UUID) -> RefreshResult:
        """Query the pod remote-control and update local records."""
```

### Processing Flow
1. Look up process by `process_id`.
2. Connect to `remote_control_address` via `CommandDispatcher` (S2.5).
3. Send `list_portals` command.
4. Send `get_trace_config` command.
5. Update `PortalSnapshot` records.
6. Return `RefreshResult` with updated data or error.

### Dependencies
- S0.1 (RegisteredProcess, PortalSnapshot models)
- S1.4 (ProcessRegistry)
- S2.5 (CommandDispatcher — may be implemented later; interface defined here)
