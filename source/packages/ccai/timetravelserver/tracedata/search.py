from dataclasses import dataclass, field
from typing import List, Optional, Set, Iterable

from ccai.timetravelserver.tracedata.events import TraceEvent, EventType
from ccai.timetravelserver.tracedata.portal_filter import PortalScopeFilter

@dataclass
class SearchQuery:
    portals: Optional[Set[str]] = None
    event_types: Optional[Set[EventType]] = None
    file_name: Optional[str] = None
    function_name: Optional[str] = None
    line_number: Optional[int] = None
    text_search: Optional[str] = None

    offset: int = 0
    limit: int = 100
    order_by: str = "timestamp"
    ascending: bool = True

@dataclass
class SearchResult:
    events: List[TraceEvent]
    total_count: int
    offset: int
    limit: int

class TraceSearchEngine:
    """
    Search and query engine over a collection of trace events.
    Applies multi-criteria filters, portal scoping, and pagination.
    """
    def __init__(self, events: Iterable[TraceEvent]):
        self.events = list(events)

    def _matches_query(self, event: TraceEvent, query: SearchQuery) -> bool:
        if query.event_types and event.event_type not in query.event_types:
            return False

        # These fields only exist on some event types
        if query.file_name or query.function_name or query.line_number is not None:
            if not hasattr(event, "file_name"):
                return False

            if query.file_name and event.file_name != query.file_name: # type: ignore
                return False
            if query.function_name and event.function_name != query.function_name: # type: ignore
                return False
            if query.line_number is not None and event.line_number != query.line_number: # type: ignore
                return False

        if query.text_search:
            text = query.text_search.lower()
            # Simple text search: check file, function, and repr of the event
            matched = False
            if hasattr(event, "file_name") and text in getattr(event, "file_name", "").lower():
                matched = True
            elif hasattr(event, "function_name") and text in getattr(event, "function_name", "").lower():
                matched = True
            elif hasattr(event, "variable_name") and text in getattr(event, "variable_name", "").lower():
                matched = True
            elif hasattr(event, "value_repr") and text in getattr(event, "value_repr", "").lower():
                matched = True

            # If not matched by specific fields, fallback to full string representation
            if not matched and text not in str(event).lower():
                return False

        return True

    def search(self, query: SearchQuery) -> SearchResult:
        # Step 1: Portal scope filtering
        filtered_events = iter(self.events)
        if query.portals:
            filtered_events = PortalScopeFilter.filter_by_portals(filtered_events, query.portals)

        # Step 2: Apply properties criteria
        matched_events = []
        for event in filtered_events:
            if self._matches_query(event, query):
                matched_events.append(event)

        # Step 3: Sorting
        # For now, we mainly support sorting by timestamp
        matched_events.sort(key=lambda e: getattr(e, query.order_by, e.timestamp), reverse=not query.ascending)

        # Step 4: Pagination
        total_count = len(matched_events)
        start_idx = query.offset
        end_idx = query.offset + query.limit

        paginated_events = matched_events[start_idx:end_idx]

        return SearchResult(
            events=paginated_events,
            total_count=total_count,
            offset=query.offset,
            limit=query.limit
        )
