# S4.3 — Portal-Scoped Filtering: Design

## Technical Architecture

### Module Layout
```
source/packages/automojo/timetravelserver/
    tracedata/
        portal_filter.py   # PortalScopeFilter
```

### Class: PortalScopeFilter

```python
class PortalScopeFilter:
    def filter_by_portal(self, events: List[TraceEvent], portal_name: str) -> List[TraceEvent]:
        """Return events within the named portal's scope."""

    def filter_by_portals(self, events: List[TraceEvent], portal_names: Set[str]) -> List[TraceEvent]:
        """Return events within any of the named portals' scopes."""
```

### Algorithm
- Track a stack of portal scopes using `PortalEnterEvent`/`PortalExitEvent`.
- Include an event if the target portal name is anywhere in the current scope stack.
- For nested filtering, check the top of the stack against the target.

### Dependencies
- S0.5 (TraceEvent, PortalEnterEvent, PortalExitEvent)
