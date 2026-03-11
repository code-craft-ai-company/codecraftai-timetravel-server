# S2.2 — Portal Activation / Deactivation: Tasks

## Implementation Tasks

- [ ] Create `debugcontrol/portal_control.py` with `PortalControlService`
- [ ] Implement `activate_portal()` — send command, update snapshot
- [ ] Implement `deactivate_portal()` — send command, update snapshot
- [ ] Implement `activate_portals()` — bulk operation
- [ ] Implement `deactivate_portals()` — bulk operation

## Testing Tasks

- [ ] Test single portal activation sends correct command
- [ ] Test single portal deactivation sends correct command
- [ ] Test bulk activation processes all portals
- [ ] Test portal snapshot is updated after activation
- [ ] Test error propagation from remote failure
- [ ] Test with unreachable process returns error
