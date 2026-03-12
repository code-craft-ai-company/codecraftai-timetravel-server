import pytest
from automojo.timetravelserver.tracedata.events import TraceEvent, EventType, CallEvent, ReturnEvent
from automojo.timetravelserver.tracedata.timeline import TimelineBuilder, Timeline

def create_mock_event(event_type: EventType, timestamp: float) -> TraceEvent:
    return TraceEvent(
        event_type=event_type,
        timestamp=timestamp,
        process_id="p1",
        session_id="s1",
        portal_name="portal"
    )

def test_build_produces_chronologically_ordered_events():
    builder = TimelineBuilder()
    builder.add_event(create_mock_event(EventType.RETURN, 2.0))
    builder.add_event(create_mock_event(EventType.CALL, 1.0))

    timeline = builder.build()

    assert len(timeline.events) == 2
    assert timeline.events[0].timestamp == 1.0
    assert timeline.events[1].timestamp == 2.0

def test_metadata_computed_correctly():
    builder = TimelineBuilder()
    builder.add_event(create_mock_event(EventType.CALL, 1.0))
    builder.add_event(create_mock_event(EventType.LINE, 1.5))
    builder.add_event(create_mock_event(EventType.RETURN, 2.0))

    timeline = builder.build()

    assert timeline.start_time == 1.0
    assert timeline.end_time == 2.0
    assert timeline.duration == 1.0
    assert timeline.event_counts == {"call": 1, "line": 1, "return": 1}

def test_merge_of_two_timelines_produces_correct_order():
    builder1 = TimelineBuilder()
    builder1.add_event(create_mock_event(EventType.CALL, 1.0))
    builder1.add_event(create_mock_event(EventType.RETURN, 3.0))
    t1 = builder1.build()

    builder2 = TimelineBuilder()
    builder2.add_event(create_mock_event(EventType.CALL, 2.0))
    builder2.add_event(create_mock_event(EventType.RETURN, 4.0))
    t2 = builder2.build()

    merged = TimelineBuilder.merge([t1, t2])

    assert len(merged.events) == 4
    assert merged.events[0].timestamp == 1.0
    assert merged.events[1].timestamp == 2.0
    assert merged.events[2].timestamp == 3.0
    assert merged.events[3].timestamp == 4.0

    assert merged.duration == 3.0
    assert merged.event_counts == {"call": 2, "return": 2}

def test_select_range_returns_only_events_within_range():
    builder = TimelineBuilder()
    builder.add_event(create_mock_event(EventType.CALL, 1.0))
    builder.add_event(create_mock_event(EventType.LINE, 2.0))
    builder.add_event(create_mock_event(EventType.RETURN, 3.0))
    timeline = builder.build()

    events = list(timeline.select_range(1.5, 2.5))
    assert len(events) == 1
    assert events[0].timestamp == 2.0

    events_from_start = list(timeline.select_range(end_time=2.0))
    assert len(events_from_start) == 2

    events_to_end = list(timeline.select_range(start_time=2.0))
    assert len(events_to_end) == 2

def test_empty_timeline_handling():
    builder = TimelineBuilder()
    timeline = builder.build()

    assert len(timeline.events) == 0
    assert timeline.start_time == 0.0
    assert timeline.end_time == 0.0
    assert timeline.duration == 0.0
    assert timeline.event_counts == {}

    merged = TimelineBuilder.merge([timeline, timeline])
    assert len(merged.events) == 0

    events = list(timeline.select_range(1.0, 2.0))
    assert len(events) == 0
