from typing import Iterable, Iterator, Set
from automojo.timetravelserver.tracedata.events import TraceEvent, EventType

class PortalScopeFilter:
    """
    Filters a sequence of TraceEvents based on portal scope.
    Tracks PORTAL_ENTER and PORTAL_EXIT events to determine current active portals.
    Assumes events are provided in chronological order.
    """

    @staticmethod
    def filter_by_portal(events: Iterable[TraceEvent], target_portal: str) -> Iterator[TraceEvent]:
        """
        Yields only events that occurred while the target_portal was active.
        PORTAL_ENTER and PORTAL_EXIT events for the target_portal are also yielded.
        """
        if not target_portal:
            return

        active_portals: Set[str] = set()

        for event in events:
            if event.event_type == EventType.PORTAL_ENTER:
                active_portals.add(event.portal_name)

            # Yield event if target portal is active
            if target_portal in active_portals:
                yield event

            if event.event_type == EventType.PORTAL_EXIT:
                if event.portal_name in active_portals:
                    active_portals.remove(event.portal_name)

    @staticmethod
    def filter_by_portals(events: Iterable[TraceEvent], target_portals: Set[str]) -> Iterator[TraceEvent]:
        """
        Yields only events that occurred while ANY of the target_portals were active.
        """
        if not target_portals:
            return

        active_portals: Set[str] = set()

        for event in events:
            if event.event_type == EventType.PORTAL_ENTER:
                active_portals.add(event.portal_name)

            # Yield event if any target portal is active
            if active_portals.intersection(target_portals):
                yield event

            if event.event_type == EventType.PORTAL_EXIT:
                if event.portal_name in active_portals:
                    active_portals.remove(event.portal_name)
