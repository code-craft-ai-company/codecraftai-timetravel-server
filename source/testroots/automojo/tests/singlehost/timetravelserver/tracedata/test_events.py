"""
    .. module:: automojo.tests.singlehost.timetravelserver.tracedata.test_events
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the Trace Event Data Model.
"""

import automojo.testbase as testbase
from automojo.timetravelserver.tracedata.events import (
    EventType,
    TraceEvent,
    CallEvent,
    ReturnEvent,
    LineEvent,
    VariableSnapshotEvent,
    PortalEnterEvent,
    PortalExitEvent,
    GatewayStartEvent,
    GatewayStopEvent,
    from_pod_event
)

def test_event_instantiation():
    event = CallEvent(
        event_type=EventType.CALL,
        timestamp=123.45,
        process_id="proc-1",
        session_id="sess-1",
        portal_name="my_portal",
        file_name="test.py",
        function_name="foo",
        line_number=10,
        arguments={"x": 1}
    )
    testbase.assert_equal(event.event_type, EventType.CALL)
    testbase.assert_equal(event.process_id, "proc-1")
    testbase.assert_equal(event.file_name, "test.py")

def test_to_dict_roundtrip():
    orig_event = ReturnEvent(
        event_type=EventType.RETURN,
        timestamp=123.5,
        process_id="p1",
        session_id="s1",
        portal_name="portal_a",
        file_name="test.py",
        function_name="foo",
        line_number=15,
        return_value="result"
    )
    data = orig_event.to_dict()
    testbase.assert_equal(data["event_type"], "return")
    testbase.assert_equal(data["return_value"], "result")

    restored_event = TraceEvent.from_dict(data)
    testbase.assert_true(isinstance(restored_event, ReturnEvent))
    testbase.assert_equal(restored_event.event_type, EventType.RETURN)
    testbase.assert_equal(restored_event.return_value, "result")
    testbase.assert_equal(restored_event.process_id, "p1")

def test_from_pod_event():
    pod_data = {
        "event_type": "line",
        "timestamp": 999.9,
        "file_name": "app.py",
        "function_name": "bar",
        "line_number": 42,
        "locals_snapshot": {"y": 2}
    }

    event = from_pod_event(pod_data, process_id="proc-99", session_id="sess-88", portal_name="portal-0")

    testbase.assert_true(isinstance(event, LineEvent))
    testbase.assert_equal(event.event_type, EventType.LINE)
    testbase.assert_equal(event.process_id, "proc-99")
    testbase.assert_equal(event.session_id, "sess-88")
    testbase.assert_equal(event.portal_name, "portal-0")
    testbase.assert_equal(event.file_name, "app.py")
    testbase.assert_equal(event.locals_snapshot, {"y": 2})

if __name__ == "__main__":
    from automojo.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
