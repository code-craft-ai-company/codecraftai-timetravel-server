# S0.5 — Trace Event Data Model (Server-Side): Tasks

## Implementation Tasks

- [ ] Create `tracedata/` package with `__init__.py`
- [ ] Create `events.py` with `EventType` discriminator constants
- [ ] Implement `TraceEvent` base dataclass with common fields and `to_dict`/`from_dict`
- [ ] Implement `CallEvent` dataclass
- [ ] Implement `ReturnEvent` dataclass
- [ ] Implement `LineEvent` dataclass
- [ ] Implement `VariableSnapshotEvent` dataclass
- [ ] Implement `PortalEnterEvent` and `PortalExitEvent` dataclasses
- [ ] Implement `GatewayStartEvent` and `GatewayStopEvent` dataclasses
- [ ] Implement `from_pod_event()` factory method
- [ ] Export all event types from `tracedata/__init__.py`

## Testing Tasks

- [ ] Test instantiation of each event type with required fields
- [ ] Test `to_dict()` round-trip for each event type
- [ ] Test `from_dict()` correctly reconstructs each event type
- [ ] Test `from_pod_event()` conversion preserves all data
- [ ] Test event_type discriminator is set correctly for each type
