# S4.6 — Search and Query Engine: Design

## Technical Architecture

### Module Layout
```
source/packages/automojo/timetravelserver/
    tracedata/
        search.py   # TraceSearchEngine, SearchQuery, SearchResult
```

### Data Models

```python
@dataclass
class SearchQuery:
    filename: Optional[str] = None
    function_name: Optional[str] = None
    line_number: Optional[int] = None
    variable_name: Optional[str] = None
    event_type: Optional[str] = None
    portal_name: Optional[str] = None
    time_start: Optional[float] = None
    time_end: Optional[float] = None
    order_by: str = "timestamp_offset"
    order_desc: bool = False
    offset: int = 0
    limit: int = 50

@dataclass
class SearchResult:
    events: List[TraceEvent]
    total_count: int
    offset: int
    limit: int

class TraceSearchEngine:
    def search(self, events: List[TraceEvent], query: SearchQuery) -> SearchResult:
        """Filter, sort, paginate events based on query criteria."""
```

### Implementation
- Apply filters sequentially as predicate functions.
- Use `PortalScopeFilter` (S4.3) for portal_name filtering.
- Text search uses case-insensitive `in` operator on string fields.
- Sort and slice for pagination.

### Dependencies
- S0.5 (TraceEvent subclasses)
- S4.3 (PortalScopeFilter)
