# S4.5 — Variable State Tracking: Design

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    tracedata/
        variable_tracker.py   # VariableTracker
```

### Class: VariableTracker

```python
@dataclass
class VariableChange:
    timestamp_offset: float
    value: Any
    filename: str
    line_number: int

class VariableTracker:
    def build_histories(self, events: List[TraceEvent]) -> Dict[str, List[VariableChange]]:
        """Build per-variable history from VariableSnapshotEvents."""

    def value_at(self, history: List[VariableChange], timestamp: float) -> Optional[Any]:
        """Return the variable value at the given timestamp (binary search)."""

    def list_variables(self, events: List[TraceEvent]) -> List[str]:
        """Return all variable names with snapshots."""

    def find_changes(self, history: List[VariableChange]) -> List[Tuple[VariableChange, VariableChange]]:
        """Return pairs of consecutive snapshots where the value differs."""
```

### Dependencies
- S0.5 (VariableSnapshotEvent)
