import pytest
from ccai.timetravelserver.tracedata.events import EventType, VariableSnapshotEvent, TraceEvent
from ccai.timetravelserver.tracedata.variable_tracker import VariableTracker, VariableChange

def create_snap(name: str, value: str, ts: float) -> VariableSnapshotEvent:
    return VariableSnapshotEvent(
        event_type=EventType.VARIABLE_SNAPSHOT, timestamp=ts, process_id="p1", session_id="s1", portal_name="portal",
        variable_name=name, value_repr=value, value_type="str", file_name="f", function_name="func", line_number=1
    )

def test_history_aggregation_groups_by_variable_name():
    tracker = VariableTracker()
    events = [
        create_snap("x", "1", 1.0),
        create_snap("y", "2", 2.0),
        create_snap("x", "3", 3.0)
    ]
    tracker.build_histories(events)

    assert tracker.list_variables() == ["x", "y"]

    x_history = tracker._histories["x"]
    assert len(x_history) == 2
    assert x_history[0].value_repr == "1"
    assert x_history[1].value_repr == "3"

def test_value_at_returns_correct_snapshot_for_given_timestamp():
    tracker = VariableTracker()
    events = [
        create_snap("x", "1", 1.0),
        create_snap("x", "2", 3.0),
        create_snap("x", "3", 5.0)
    ]
    tracker.build_histories(events)

    assert tracker.value_at("x", 2.0).value_repr == "1"
    assert tracker.value_at("x", 3.0).value_repr == "2"
    assert tracker.value_at("x", 4.0).value_repr == "2"
    assert tracker.value_at("x", 5.0).value_repr == "3"
    assert tracker.value_at("x", 6.0).value_repr == "3"

def test_value_at_returns_none_before_any_snapshot():
    tracker = VariableTracker()
    events = [
        create_snap("x", "1", 2.0)
    ]
    tracker.build_histories(events)

    assert tracker.value_at("x", 1.0) is None

def test_list_variables_returns_all_unique_names():
    tracker = VariableTracker()
    events = [
        create_snap("x", "1", 1.0),
        create_snap("y", "2", 2.0),
        create_snap("z", "3", 3.0)
    ]
    tracker.build_histories(events)

    variables = tracker.list_variables()
    assert set(variables) == {"x", "y", "z"}

def test_find_changes_identifies_value_transitions():
    tracker = VariableTracker()
    events = [
        create_snap("x", "1", 1.0),
        create_snap("x", "1", 2.0), # No change
        create_snap("x", "2", 3.0),
        create_snap("x", "2", 4.0)  # No change
    ]
    tracker.build_histories(events)

    changes = tracker.find_changes("x")
    assert len(changes) == 2

    assert changes[0].timestamp == 1.0
    assert changes[0].old_value_repr is None
    assert changes[0].new_value_repr == "1"

    assert changes[1].timestamp == 3.0
    assert changes[1].old_value_repr == "1"
    assert changes[1].new_value_repr == "2"
