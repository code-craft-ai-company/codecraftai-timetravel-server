# S4.2 — Timeline Reconstruction: Design

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    tracedata/
        timeline.py   # TimelineBuilder
```

### Class: TimelineBuilder

```python
class TimelineBuilder:
    def build(self, events: Iterable[TraceEvent]) -> Timeline:
        """Sort events into a chronological timeline."""

    def merge(self, *timelines: Timeline) -> Timeline:
        """Merge multiple timelines into one ordered timeline."""

    def select_range(self, timeline: Timeline, start: float, end: float) -> Timeline:
        """Return events within [start, end] timestamp range."""

@dataclass
class Timeline:
    events: List[TraceEvent]
    duration: float
    event_count: int
    event_type_counts: Dict[str, int]
    earliest: float
    latest: float
```

### Merge Algorithm
- Heap-merge (heapq.merge) on `timestamp_offset` for efficient multi-source merge.

### Dependencies
- S0.5 (TraceEvent)
- S4.1 (TraceFileReader — provides events)
