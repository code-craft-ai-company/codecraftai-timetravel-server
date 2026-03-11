# S2.1 — Portal Discovery: Tasks

## Implementation Tasks

- [ ] Create `debugcontrol/` package with `__init__.py`
- [ ] Create `debugcontrol/portal_discovery.py` with `PortalDiscoveryService`
- [ ] Implement `discover()` — send `list_portals`, parse response, update snapshots
- [ ] Define `PortalInfo` dataclass (name, is_active)

## Testing Tasks

- [ ] Test discovery returns portal list from mock remote
- [ ] Test discovery updates portal snapshots in database
- [ ] Test discovery handles connection failure gracefully
- [ ] Test discovery with unknown process_id returns error
