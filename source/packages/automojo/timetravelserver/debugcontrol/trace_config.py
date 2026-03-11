import uuid
from dataclasses import dataclass
from typing import Callable, Optional

from sqlalchemy.orm import Session

from automojo.timetravelserver.registration.process_registry import ProcessRegistry
from automojo.timetravelserver.debugcontrol.command_dispatcher import CommandDispatcher

@dataclass
class TraceConfigInfo:
    granularity: str
    record_inner_portals: bool

class TraceConfigService:
    def __init__(self, session_factory: Callable[[], Session], command_dispatcher: CommandDispatcher, process_registry: ProcessRegistry):
        self._session_factory = session_factory
        self._command_dispatcher = command_dispatcher
        self._process_registry = process_registry

    def get_config(self, process_id: uuid.UUID) -> TraceConfigInfo:
        """Query pod for current trace configuration."""
        process = self._process_registry.get_process(process_id)
        if not process:
            raise ValueError(f"Process with ID {process_id} not found.")
        if not process.remote_control_address:
            raise ValueError(f"Process {process_id} has no remote control address.")

        response = self._command_dispatcher.dispatch(
            process.remote_control_address,
            "get_trace_config"
        )

        return TraceConfigInfo(
            granularity=response.get("granularity", "call_return"),
            record_inner_portals=response.get("record_inner_portals", False)
        )

    def update_config(self, process_id: uuid.UUID, granularity: Optional[str] = None,
                      record_inner_portals: Optional[bool] = None) -> TraceConfigInfo:
        """Update trace configuration on the pod."""
        process = self._process_registry.get_process(process_id)
        if not process:
            raise ValueError(f"Process with ID {process_id} not found.")
        if not process.remote_control_address:
            raise ValueError(f"Process {process_id} has no remote control address.")

        params = {}
        if granularity is not None:
            if granularity not in ("call_return", "line_level", "variable_snapshot"):
                raise ValueError(f"Invalid granularity: {granularity}")
            params["granularity"] = granularity
        if record_inner_portals is not None:
            params["record_inner_portals"] = record_inner_portals

        response = self._command_dispatcher.dispatch(
            process.remote_control_address,
            "update_trace_config",
            params
        )

        return TraceConfigInfo(
            granularity=response.get("granularity", "call_return"),
            record_inner_portals=response.get("record_inner_portals", False)
        )
