from dataclasses import dataclass, field
from typing import List, Optional, Dict, Iterable

from ccai.timetravelserver.tracedata.events import TraceEvent, EventType, CallEvent, ReturnEvent

@dataclass
class CallGraphNode:
    call_event: CallEvent
    return_event: Optional[ReturnEvent] = None
    children: List["CallGraphNode"] = field(default_factory=list)
    parent: Optional["CallGraphNode"] = None

    @property
    def duration(self) -> Optional[float]:
        if self.return_event:
            return self.return_event.timestamp - self.call_event.timestamp
        return None

class CallGraphBuilder:
    """
    Builds a call graph from a sequence of TraceEvents.
    Maintains separate graphs per thread/process.
    """
    def __init__(self):
        # We'll use a single key for "thread separation".
        # Assuming we separate by process_id and session_id as the surrogate for "thread"
        # since thread_id isn't explicitly in TraceEvent.
        # Actually, let's just use process_id + session_id
        self.roots: Dict[str, List[CallGraphNode]] = {}
        self._stacks: Dict[str, List[CallGraphNode]] = {}

    def add_events(self, events: Iterable[TraceEvent]) -> None:
        for event in events:
            # We construct a key per thread/process
            key = f"{event.process_id}:{event.session_id}"

            if key not in self.roots:
                self.roots[key] = []
                self._stacks[key] = []

            stack = self._stacks[key]

            if event.event_type == EventType.CALL:
                node = CallGraphNode(call_event=event) # type: ignore
                if stack:
                    # Parent is the current top of stack
                    parent = stack[-1]
                    parent.children.append(node)
                    node.parent = parent
                else:
                    # Root node
                    self.roots[key].append(node)
                stack.append(node)

            elif event.event_type == EventType.RETURN:
                if stack:
                    # Pop the current call and attach return event
                    node = stack.pop()
                    node.return_event = event # type: ignore
                else:
                    # Unmatched return, ignore or handle?
                    pass

    def get_roots(self, process_id: str, session_id: str) -> List[CallGraphNode]:
        key = f"{process_id}:{session_id}"
        return self.roots.get(key, [])
