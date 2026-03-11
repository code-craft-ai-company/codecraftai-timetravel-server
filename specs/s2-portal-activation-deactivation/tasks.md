# S2.2 — Portal Activation / Deactivation: Tasks

## Implementation Tasks

- [x] Create `debugcontrol/portal_control.py` with `PortalControlService`
- [x] Implement `activate_portal()` — send command, update snapshot
- [x] Implement `deactivate_portal()` — send command, update snapshot
- [x] Implement `activate_portals()` — bulk operation
- [x] Implement `deactivate_portals()` — bulk operation

## Testing Tasks

- [x] Test single portal activation sends correct command
- [x] Test single portal deactivation sends correct command
- [x] Test bulk activation processes all portals
- [x] Test portal snapshot is updated after activation
- [x] Test error propagation from remote failure
- [x] Test with unreachable process returns error
