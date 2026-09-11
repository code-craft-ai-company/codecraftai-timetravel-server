"""
    .. module:: ccai.tests.singlehost.timetravelserver.tracedata.test_portal_filter
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the PortalScopeFilter.
"""

from ccai.timetravelserver.tracedata.events import TraceEvent, EventType, PortalEnterEvent, PortalExitEvent
from ccai.timetravelserver.tracedata.portal_filter import PortalScopeFilter

def create_event(event_type: EventType, portal_name: str, timestamp: float) -> TraceEvent:
    # Use PortalEnterEvent / PortalExitEvent specifically for portal events
    if event_type == EventType.PORTAL_ENTER:
        return PortalEnterEvent(event_type=event_type, timestamp=timestamp, process_id="p", session_id="s", portal_name=portal_name)
    elif event_type == EventType.PORTAL_EXIT:
        return PortalExitEvent(event_type=event_type, timestamp=timestamp, process_id="p", session_id="s", portal_name=portal_name)
    else:
        return TraceEvent(event_type=event_type, timestamp=timestamp, process_id="p", session_id="s", portal_name=portal_name)

def test_filtering_returns_only_events_within_target_portal():
    events = [
        create_event(EventType.CALL, "portal_a", 1.0),
        create_event(EventType.PORTAL_ENTER, "portal_b", 2.0),
        create_event(EventType.LINE, "portal_b", 3.0),
        create_event(EventType.PORTAL_EXIT, "portal_b", 4.0),
        create_event(EventType.RETURN, "portal_a", 5.0)
    ]

    filtered = list(PortalScopeFilter.filter_by_portal(events, "portal_b"))
    assert len(filtered) == 3
    assert filtered[0].timestamp == 2.0
    assert filtered[1].timestamp == 3.0
    assert filtered[2].timestamp == 4.0

def test_nested_portal_filtering():
    events = [
        create_event(EventType.PORTAL_ENTER, "portal_a", 1.0),
        create_event(EventType.CALL, "portal_a", 2.0),
        create_event(EventType.PORTAL_ENTER, "portal_b", 3.0),
        create_event(EventType.LINE, "portal_b", 4.0),
        create_event(EventType.PORTAL_EXIT, "portal_b", 5.0),
        create_event(EventType.PORTAL_EXIT, "portal_a", 6.0)
    ]

    filtered_a = list(PortalScopeFilter.filter_by_portal(events, "portal_a"))
    assert len(filtered_a) == 6

    filtered_b = list(PortalScopeFilter.filter_by_portal(events, "portal_b"))
    assert len(filtered_b) == 3
    assert filtered_b[0].timestamp == 3.0
    assert filtered_b[1].timestamp == 4.0
    assert filtered_b[2].timestamp == 5.0

def test_multi_portal_filtering():
    events = [
        create_event(EventType.PORTAL_ENTER, "portal_a", 1.0),
        create_event(EventType.CALL, "portal_a", 2.0),
        create_event(EventType.PORTAL_EXIT, "portal_a", 3.0),
        create_event(EventType.PORTAL_ENTER, "portal_b", 4.0),
        create_event(EventType.LINE, "portal_b", 5.0),
        create_event(EventType.PORTAL_EXIT, "portal_b", 6.0),
        create_event(EventType.PORTAL_ENTER, "portal_c", 7.0),
        create_event(EventType.RETURN, "portal_c", 8.0),
        create_event(EventType.PORTAL_EXIT, "portal_c", 9.0)
    ]

    filtered = list(PortalScopeFilter.filter_by_portals(events, {"portal_a", "portal_c"}))
    assert len(filtered) == 6
    timestamps = [e.timestamp for e in filtered]
    assert timestamps == [1.0, 2.0, 3.0, 7.0, 8.0, 9.0]

def test_empty_portal_name_returns_no_events():
    events = [
        create_event(EventType.PORTAL_ENTER, "portal_a", 1.0),
        create_event(EventType.CALL, "portal_a", 2.0),
        create_event(EventType.PORTAL_EXIT, "portal_a", 3.0)
    ]

    filtered = list(PortalScopeFilter.filter_by_portal(events, ""))
    assert len(filtered) == 0

    filtered_multi = list(PortalScopeFilter.filter_by_portals(events, set()))
    assert len(filtered_multi) == 0

def test_events_outside_any_portal_are_excluded():
    events = [
        create_event(EventType.CALL, "none", 1.0),
        create_event(EventType.LINE, "none", 2.0),
        create_event(EventType.RETURN, "none", 3.0)
    ]

    filtered = list(PortalScopeFilter.filter_by_portal(events, "portal_a"))
    assert len(filtered) == 0


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
