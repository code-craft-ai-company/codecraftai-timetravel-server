"""
    .. module:: ccai.tests.singlehost.timetravelserver.tracedata.test_search
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the TraceSearchEngine.
"""

from typing import List

from ccai.timetravelserver.tracedata.events import TraceEvent, EventType, CallEvent, LineEvent, VariableSnapshotEvent
from ccai.timetravelserver.tracedata.search import TraceSearchEngine, SearchQuery, SearchResult

def create_call(ts: float, file: str, func: str) -> CallEvent:
    return CallEvent(
        event_type=EventType.CALL, timestamp=ts, process_id="p1", session_id="s1", portal_name="portal",
        file_name=file, function_name=func, line_number=1, arguments={}
    )

def create_line(ts: float, file: str, func: str, line: int) -> LineEvent:
    return LineEvent(
        event_type=EventType.LINE, timestamp=ts, process_id="p1", session_id="s1", portal_name="portal",
        file_name=file, function_name=func, line_number=line, locals_snapshot={}
    )

def create_var(ts: float, var: str, val: str) -> VariableSnapshotEvent:
    return VariableSnapshotEvent(
        event_type=EventType.VARIABLE_SNAPSHOT, timestamp=ts, process_id="p1", session_id="s1", portal_name="portal",
        file_name="f", function_name="func", line_number=1, variable_name=var, value_repr=val, value_type="str"
    )

def create_sample_events() -> List[TraceEvent]:
    """
        Builds the fixed set of six events every search test runs against.
    """
    events = [
        create_call(1.0, "main.py", "start"),
        create_line(2.0, "main.py", "start", 10),
        create_var(3.0, "x", "100"),
        create_call(4.0, "utils.py", "helper"),
        create_line(5.0, "utils.py", "helper", 20),
        create_var(6.0, "y", "hello world")
    ]
    return events

def test_single_criterion_filtering():
    sample_events = create_sample_events()
    engine = TraceSearchEngine(sample_events)

    # By filename
    res = engine.search(SearchQuery(file_name="utils.py"))
    assert res.total_count == 2

    # By function
    res = engine.search(SearchQuery(function_name="start"))
    assert res.total_count == 2

    # By line
    res = engine.search(SearchQuery(line_number=20))
    assert res.total_count == 1

    # By event type
    res = engine.search(SearchQuery(event_types={EventType.VARIABLE_SNAPSHOT}))
    assert res.total_count == 2

def test_multi_criteria_combination():
    sample_events = create_sample_events()
    engine = TraceSearchEngine(sample_events)

    # By filename and event type
    query = SearchQuery(file_name="main.py", event_types={EventType.LINE})
    res = engine.search(query)

    assert res.total_count == 1
    assert res.events[0].event_type == EventType.LINE
    assert res.events[0].file_name == "main.py"

def test_partial_text_search_matching():
    sample_events = create_sample_events()
    engine = TraceSearchEngine(sample_events)

    # Match in function name
    res = engine.search(SearchQuery(text_search="help"))
    assert res.total_count == 2 # call to helper, line in helper

    # Match in variable value
    res = engine.search(SearchQuery(text_search="world"))
    assert res.total_count == 1
    assert res.events[0].value_repr == "hello world"

def test_pagination_offset_and_limit():
    sample_events = create_sample_events()
    engine = TraceSearchEngine(sample_events)

    # Total 6 events
    res1 = engine.search(SearchQuery(offset=0, limit=2))
    assert len(res1.events) == 2
    assert res1.events[0].timestamp == 1.0

    res2 = engine.search(SearchQuery(offset=2, limit=2))
    assert len(res2.events) == 2
    assert res2.events[0].timestamp == 3.0

def test_total_count_is_correct_regardless_of_pagination():
    sample_events = create_sample_events()
    engine = TraceSearchEngine(sample_events)

    res = engine.search(SearchQuery(offset=2, limit=2))
    assert res.total_count == 6
    assert len(res.events) == 2

def test_ordering_ascending_and_descending():
    sample_events = create_sample_events()
    engine = TraceSearchEngine(sample_events)

    # Descending
    res_desc = engine.search(SearchQuery(ascending=False))
    assert res_desc.events[0].timestamp == 6.0
    assert res_desc.events[-1].timestamp == 1.0

    # Ascending
    res_asc = engine.search(SearchQuery(ascending=True))
    assert res_asc.events[0].timestamp == 1.0
    assert res_asc.events[-1].timestamp == 6.0


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
