# S2.2 — Portal Activation / Deactivation: Design

## Overview
Service methods to control portal activation state on remote processes via the command dispatcher.

## Technical Architecture

### Module Layout
```
source/packages/automojo/timetravelserver/
    debugcontrol/
        portal_control.py   # PortalControlService
```

### Class: PortalControlService

```python
class PortalControlService:
    def __init__(self, session_factory, command_dispatcher: CommandDispatcher):
        ...

    def activate_portal(self, process_id: UUID, portal_name: str) -> bool:
        """Activate a single portal. Returns True on success."""

    def deactivate_portal(self, process_id: UUID, portal_name: str) -> bool:
        """Deactivate a single portal. Returns True on success."""

    def activate_portals(self, process_id: UUID, portal_names: List[str]) -> Dict[str, bool]:
        """Bulk activate. Returns {name: success} map."""

    def deactivate_portals(self, process_id: UUID, portal_names: List[str]) -> Dict[str, bool]:
        """Bulk deactivate. Returns {name: success} map."""
```

### Processing Flow
1. Look up process remote address.
2. Send `activate_portal`/`deactivate_portal` command via CommandDispatcher.
3. Parse response for success/error.
4. Update local `PortalSnapshot`.
5. Return result.

### Dependencies
- S0.1 (PortalSnapshot model)
- S1.4 (ProcessRegistry)
- S2.5 (CommandDispatcher)
