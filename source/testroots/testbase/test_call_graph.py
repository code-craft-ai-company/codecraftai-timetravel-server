import pytest
from automojo.timetravelserver.tracedata.events import TraceEvent, EventType, CallEvent, ReturnEvent
from automojo.timetravelserver.tracedata.call_graph import CallGraphBuilder, CallGraphNode

def create_call(name: str, ts: float, process_id="p1", session_id="s1") -> CallEvent:
    return CallEvent(
        event_type=EventType.CALL, timestamp=ts, process_id=process_id, session_id=session_id, portal_name="",
        file_name="f", function_name=name, line_number=1, arguments={}
    )

def create_return(name: str, ts: float, process_id="p1", session_id="s1") -> ReturnEvent:
    return ReturnEvent(
        event_type=EventType.RETURN, timestamp=ts, process_id=process_id, session_id=session_id, portal_name="",
        file_name="f", function_name=name, line_number=1, return_value=None
    )

def test_simple_linear_call_graph():
    builder = CallGraphBuilder()
    events = [
        create_call("A", 1.0),
        create_call("B", 2.0),
        create_call("C", 3.0),
        create_return("C", 4.0),
        create_return("B", 5.0),
        create_return("A", 6.0)
    ]
    builder.add_events(events)
    roots = builder.get_roots("p1", "s1")

    assert len(roots) == 1
    node_a = roots[0]
    assert node_a.call_event.function_name == "A"

    assert len(node_a.children) == 1
    node_b = node_a.children[0]
    assert node_b.call_event.function_name == "B"

    assert len(node_b.children) == 1
    node_c = node_b.children[0]
    assert node_c.call_event.function_name == "C"

def test_nested_recursive_call_graph():
    builder = CallGraphBuilder()
    events = [
        create_call("A", 1.0),
        create_call("A", 2.0),
        create_return("A", 3.0),
        create_return("A", 4.0)
    ]
    builder.add_events(events)
    roots = builder.get_roots("p1", "s1")

    assert len(roots) == 1
    root = roots[0]
    assert root.call_event.timestamp == 1.0

    assert len(root.children) == 1
    child = root.children[0]
    assert child.call_event.timestamp == 2.0
    assert child.return_event.timestamp == 3.0

    assert root.return_event.timestamp == 4.0

def test_multi_thread_produces_separate_graphs():
    builder = CallGraphBuilder()
    events = [
        create_call("T1", 1.0, process_id="p1"),
        create_call("T2", 2.0, process_id="p2"),
        create_return("T1", 3.0, process_id="p1"),
        create_return("T2", 4.0, process_id="p2")
    ]
    builder.add_events(events)

    t1_roots = builder.get_roots("p1", "s1")
    t2_roots = builder.get_roots("p2", "s1")

    assert len(t1_roots) == 1
    assert t1_roots[0].call_event.function_name == "T1"

    assert len(t2_roots) == 1
    assert t2_roots[0].call_event.function_name == "T2"

def test_timing_data_accuracy():
    builder = CallGraphBuilder()
    events = [
        create_call("A", 1.5),
        create_return("A", 4.0)
    ]
    builder.add_events(events)
    roots = builder.get_roots("p1", "s1")

    assert len(roots) == 1
    node = roots[0]
    assert node.duration == 2.5

def test_unmatched_call_event_handling():
    builder = CallGraphBuilder()
    events = [
        create_call("A", 1.0),
        create_call("B", 2.0)
    ]
    builder.add_events(events)
    roots = builder.get_roots("p1", "s1")

    assert len(roots) == 1
    root = roots[0]

    assert root.duration is None
    assert root.return_event is None

    assert root.children[0].duration is None
