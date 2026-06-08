from enum import Enum
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

class EventType(str, Enum):
    CALL = "call"
    RETURN = "return"
    LINE = "line"
    VARIABLE_SNAPSHOT = "variable_snapshot"
    PORTAL_ENTER = "portal_enter"
    PORTAL_EXIT = "portal_exit"
    GATEWAY_START = "gateway_start"
    GATEWAY_STOP = "gateway_stop"

@dataclass
class TraceEvent:
    event_type: EventType
    timestamp: float
    process_id: str
    session_id: str
    portal_name: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TraceEvent":
        event_type = EventType(data["event_type"])
        data_copy = dict(data)
        data_copy["event_type"] = event_type

        if event_type == EventType.CALL:
            return CallEvent(**data_copy)
        elif event_type == EventType.RETURN:
            return ReturnEvent(**data_copy)
        elif event_type == EventType.LINE:
            return LineEvent(**data_copy)
        elif event_type == EventType.VARIABLE_SNAPSHOT:
            return VariableSnapshotEvent(**data_copy)
        elif event_type == EventType.PORTAL_ENTER:
            return PortalEnterEvent(**data_copy)
        elif event_type == EventType.PORTAL_EXIT:
            return PortalExitEvent(**data_copy)
        elif event_type == EventType.GATEWAY_START:
            return GatewayStartEvent(**data_copy)
        elif event_type == EventType.GATEWAY_STOP:
            return GatewayStopEvent(**data_copy)
        else:
            return TraceEvent(**data_copy)

@dataclass
class CallEvent(TraceEvent):
    file_name: str
    function_name: str
    line_number: int
    arguments: Dict[str, Any]

@dataclass
class ReturnEvent(TraceEvent):
    file_name: str
    function_name: str
    line_number: int
    return_value: Any

@dataclass
class LineEvent(TraceEvent):
    file_name: str
    function_name: str
    line_number: int
    locals_snapshot: Optional[Dict[str, Any]] = None

@dataclass
class VariableSnapshotEvent(TraceEvent):
    variable_name: str
    value_repr: str
    value_type: str
    file_name: str
    function_name: str
    line_number: int

@dataclass
class PortalEnterEvent(TraceEvent):
    pass

@dataclass
class PortalExitEvent(TraceEvent):
    pass

@dataclass
class GatewayStartEvent(TraceEvent):
    pass

@dataclass
class GatewayStopEvent(TraceEvent):
    pass

def from_pod_event(pod_data: Dict[str, Any], process_id: str, session_id: str, portal_name: str) -> TraceEvent:
    """Factory to create a TraceEvent from a pod-emitted event dictionary."""
    data = dict(pod_data)
    data["process_id"] = process_id
    data["session_id"] = session_id
    data["portal_name"] = portal_name
    return TraceEvent.from_dict(data)
