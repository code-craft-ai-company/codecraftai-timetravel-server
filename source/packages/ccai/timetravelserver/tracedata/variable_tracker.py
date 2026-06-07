import bisect
from typing import List, Dict, Optional, Iterable
from dataclasses import dataclass

from ccai.timetravelserver.tracedata.events import TraceEvent, EventType, VariableSnapshotEvent

@dataclass
class VariableChange:
    timestamp: float
    old_value_repr: Optional[str]
    new_value_repr: str
    variable_name: str

class VariableTracker:
    def __init__(self):
        # Maps variable_name to a sorted list of VariableSnapshotEvent
        self._histories: Dict[str, List[VariableSnapshotEvent]] = {}
        # Precomputed list of timestamps per variable for fast bisect
        self._timestamps: Dict[str, List[float]] = {}

    def build_histories(self, events: Iterable[TraceEvent]) -> None:
        """
        Aggregates VariableSnapshotEvents by variable name and sorts them by timestamp.
        """
        for event in events:
            if event.event_type == EventType.VARIABLE_SNAPSHOT:
                snap_event: VariableSnapshotEvent = event # type: ignore
                var_name = snap_event.variable_name

                if var_name not in self._histories:
                    self._histories[var_name] = []
                self._histories[var_name].append(snap_event)

        # Sort each history by timestamp and prepare timestamp lists for bisect
        for var_name in self._histories:
            self._histories[var_name].sort(key=lambda e: e.timestamp)
            self._timestamps[var_name] = [e.timestamp for e in self._histories[var_name]]

    def value_at(self, variable_name: str, timestamp: float) -> Optional[VariableSnapshotEvent]:
        """
        Returns the variable snapshot in effect at the given timestamp using binary search.
        If the timestamp is before the first snapshot, returns None.
        """
        if variable_name not in self._timestamps:
            return None

        timestamps = self._timestamps[variable_name]

        # bisect_right returns the insertion point which is exactly one past the last element <= timestamp
        idx = bisect.bisect_right(timestamps, timestamp)

        if idx == 0:
            return None

        return self._histories[variable_name][idx - 1]

    def list_variables(self) -> List[str]:
        """
        Returns a list of all unique variable names tracked.
        """
        return list(self._histories.keys())

    def find_changes(self, variable_name: str) -> List[VariableChange]:
        """
        Identifies value change points for a variable.
        """
        if variable_name not in self._histories:
            return []

        changes = []
        history = self._histories[variable_name]

        prev_value = None

        for event in history:
            if prev_value != event.value_repr:
                changes.append(
                    VariableChange(
                        timestamp=event.timestamp,
                        old_value_repr=prev_value,
                        new_value_repr=event.value_repr,
                        variable_name=variable_name
                    )
                )
                prev_value = event.value_repr

        return changes
