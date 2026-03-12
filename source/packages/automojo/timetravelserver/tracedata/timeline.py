from dataclasses import dataclass, field
from typing import List, Iterable, Iterator, Dict, Any, Optional
import heapq

from automojo.timetravelserver.tracedata.events import TraceEvent

@dataclass
class Timeline:
    events: List[TraceEvent]
    start_time: float = 0.0
    end_time: float = 0.0
    duration: float = 0.0
    event_counts: Dict[str, int] = field(default_factory=dict)

    def select_range(self, start_time: Optional[float] = None, end_time: Optional[float] = None) -> Iterator[TraceEvent]:
        """Returns events within the specified timestamp range (inclusive)."""
        for event in self.events:
            if start_time is not None and event.timestamp < start_time:
                continue
            if end_time is not None and event.timestamp > end_time:
                # Assuming events are sorted by timestamp
                break
            yield event

class TimelineBuilder:
    def __init__(self):
        self.events: List[TraceEvent] = []

    def add_event(self, event: TraceEvent) -> None:
        self.events.append(event)

    def add_events(self, events: Iterable[TraceEvent]) -> None:
        self.events.extend(events)

    def build(self) -> Timeline:
        """
        Sorts the accumulated events by timestamp, computes metadata (duration, event counts),
        and returns a Timeline object.
        """
        # Sort events by timestamp
        self.events.sort(key=lambda e: e.timestamp)

        start_time = 0.0
        end_time = 0.0
        duration = 0.0
        event_counts: Dict[str, int] = {}

        if self.events:
            start_time = self.events[0].timestamp
            end_time = self.events[-1].timestamp
            duration = end_time - start_time

            for event in self.events:
                event_type_str = event.event_type.value
                event_counts[event_type_str] = event_counts.get(event_type_str, 0) + 1

        return Timeline(
            events=self.events,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            event_counts=event_counts
        )

    @staticmethod
    def merge(timelines: List[Timeline]) -> Timeline:
        """
        Merges multiple Timeline objects into a single new Timeline.
        Uses heapq.merge since the constituent timelines' events are already sorted.
        """
        merged_events_iter = heapq.merge(*(t.events for t in timelines), key=lambda e: e.timestamp)
        merged_events = list(merged_events_iter)

        start_time = 0.0
        end_time = 0.0
        duration = 0.0
        event_counts: Dict[str, int] = {}

        if merged_events:
            start_time = merged_events[0].timestamp
            end_time = merged_events[-1].timestamp
            duration = end_time - start_time

            # Combine counts
            for t in timelines:
                for k, v in t.event_counts.items():
                    event_counts[k] = event_counts.get(k, 0) + v

        return Timeline(
            events=merged_events,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            event_counts=event_counts
        )
