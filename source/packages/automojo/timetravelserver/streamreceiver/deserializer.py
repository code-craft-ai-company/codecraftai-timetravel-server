import struct
import pickle
import logging
from typing import BinaryIO, Iterator, Any, Dict
from automojo.timetravelserver.tracedata.events import TraceEvent, EventType, CallEvent, ReturnEvent, LineEvent

logger = logging.getLogger(__name__)

class HybridFormatDeserializer:
    # Envelope format:
    # [1 byte event_type length][event_type bytes][8 bytes timestamp (double)][4 bytes payload_length][payload_length bytes payload]
    # We will use string length + string for event type since EventType is string enum
    # We'll use a slightly different envelope: [1 byte type len][type str][8 byte double ts][4 byte payload len][payload]

    def deserialize_stream(self, stream: BinaryIO, process_id: str, session_id: str, portal_name: str) -> Iterator[TraceEvent]:
        """
        Reads from a binary stream, parses envelopes, and yields TraceEvent objects.
        Handles corruption by skipping to the next valid envelope if possible (though
        without a magic number, recovery is limited).
        """
        while True:
            # Read type length
            type_len_data = stream.read(1)
            if not type_len_data:
                break

            type_len = type_len_data[0]

            # Read type string
            type_str_data = stream.read(type_len)
            if len(type_str_data) < type_len:
                break

            try:
                event_type_str = type_str_data.decode('utf-8')
                event_type = EventType(event_type_str)
            except ValueError:
                logger.error(f"Invalid event type: {type_str_data}")
                break

            # Read timestamp (double) and payload len (unsigned int)
            header_data = stream.read(12)
            if len(header_data) < 12:
                break

            timestamp, payload_length = struct.unpack("!d I", header_data)

            # Read payload
            payload_data = stream.read(payload_length)
            if len(payload_data) < payload_length:
                logger.warning(f"Incomplete payload read. Expected {payload_length}, got {len(payload_data)}. Stream ended early.")
                break

            try:
                payload = pickle.loads(payload_data)
            except Exception as e:
                logger.error(f"Failed to deserialize payload: {e}. Skipping event.")
                continue

            try:
                event = self._materialize_event(event_type, timestamp, process_id, session_id, portal_name, payload)
                yield event
            except Exception as e:
                logger.error(f"Failed to materialize event: {e}. Payload was: {payload}")
                continue

    def _materialize_event(self, event_type: EventType, timestamp: float, process_id: str, session_id: str, portal_name: str, payload: Dict[str, Any]) -> TraceEvent:
        data = dict(payload)
        data["event_type"] = event_type.value
        data["timestamp"] = timestamp
        data["process_id"] = process_id
        data["session_id"] = session_id
        data["portal_name"] = portal_name

        return TraceEvent.from_dict(data)
