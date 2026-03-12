import logging
import threading
from typing import Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)

class FlowControlStatus(Enum):
    OK = "OK"
    PAUSE = "PAUSE"
    RESUME = "RESUME"

class FlowController:
    def __init__(self, high_watermark: int, low_watermark: int, global_memory_limit: int):
        self.high_watermark = high_watermark
        self.low_watermark = low_watermark
        self.global_memory_limit = global_memory_limit

        self.global_memory_used = 0
        self.connection_buffers: Dict[str, int] = {}
        self.connection_states: Dict[str, FlowControlStatus] = {}
        self._lock = threading.Lock()

    def register_connection(self, connection_id: str):
        with self._lock:
            if connection_id not in self.connection_buffers:
                self.connection_buffers[connection_id] = 0
                self.connection_states[connection_id] = FlowControlStatus.OK

    def unregister_connection(self, connection_id: str):
        with self._lock:
            if connection_id in self.connection_buffers:
                size = self.connection_buffers.pop(connection_id)
                self.global_memory_used -= size
            self.connection_states.pop(connection_id, None)

    def should_accept_new(self) -> bool:
        """Returns True if the global memory limit has not been exceeded."""
        with self._lock:
            return self.global_memory_used < self.global_memory_limit

    def update_buffer_size(self, connection_id: str, new_size: int) -> FlowControlStatus:
        """
        Updates the buffer size for a connection and returns the flow control command
        (PAUSE, RESUME, or OK) based on high/low watermarks.
        """
        with self._lock:
            if connection_id not in self.connection_buffers:
                return FlowControlStatus.OK

            old_size = self.connection_buffers[connection_id]
            self.connection_buffers[connection_id] = new_size

            # Update global memory
            self.global_memory_used += (new_size - old_size)

            current_state = self.connection_states[connection_id]

            if current_state == FlowControlStatus.OK or current_state == FlowControlStatus.RESUME:
                if new_size >= self.high_watermark:
                    self.connection_states[connection_id] = FlowControlStatus.PAUSE
                    return FlowControlStatus.PAUSE
            elif current_state == FlowControlStatus.PAUSE:
                if new_size <= self.low_watermark:
                    self.connection_states[connection_id] = FlowControlStatus.RESUME
                    return FlowControlStatus.RESUME

            return FlowControlStatus.OK
