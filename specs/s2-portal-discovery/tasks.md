# S2.1 — Portal Discovery: Tasks

## Implementation Tasks

- [x] Create `debugcontrol/` package with `__init__.py`
- [x] Create `debugcontrol/portal_discovery.py` with `PortalDiscoveryService`
- [x] Implement `discover()` — send `list_portals`, parse response, update snapshots
- [x] Define `PortalInfo` dataclass (name, is_active)

## Testing Tasks

- [x] Test discovery returns portal list from mock remote
- [x] Test discovery updates portal snapshots in database
- [x] Test discovery handles connection failure gracefully
- [x] Test discovery with unknown process_id returns error
