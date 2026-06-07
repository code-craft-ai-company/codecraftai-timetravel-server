# S2.1 — Portal Discovery: Design

## Overview
Uses the command dispatcher (S2.5) to query a pod's portal registry and update local snapshot records.

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    debugcontrol/
        __init__.py
        portal_discovery.py   # PortalDiscoveryService
```

### Class: PortalDiscoveryService

```python
class PortalDiscoveryService:
    def __init__(self, session_factory, command_dispatcher: CommandDispatcher):
        ...

    def discover(self, process_id: UUID) -> List[PortalInfo]:
        """Query pod for portals and update local snapshots."""
```

### Processing Flow
1. Look up process `remote_control_address`.
2. Send `list_portals` via `CommandDispatcher`.
3. Parse response into `PortalInfo` list.
4. Upsert `PortalSnapshot` records.
5. Return portal list.

### Dependencies
- S0.1 (PortalSnapshot model)
- S1.4 (ProcessRegistry)
- S2.5 (CommandDispatcher)
