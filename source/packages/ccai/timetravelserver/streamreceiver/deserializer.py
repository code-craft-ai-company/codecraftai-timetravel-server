import io
import os
import struct
import pickle
import logging
from typing import BinaryIO, Iterator, Any, Dict, FrozenSet, Tuple
from ccai.timetravelserver.tracedata.events import TraceEvent, EventType, CallEvent, ReturnEvent, LineEvent

logger = logging.getLogger(__name__)


# Trace payloads are plain data dictionaries (function names, line numbers, and
# argument/return/local *values* that the pod has already reduced to primitive
# representations before transmission).  The payload arrives over a network
# socket, so it is UNTRUSTED input -- a bare ``pickle.loads`` here is a
# remote-code-execution vector, because a malicious peer can embed a
# ``__reduce__`` gadget that imports ``os``/``subprocess`` and runs arbitrary
# code while the stream is being decoded.  We therefore restrict unpickling to a
# fixed allow-list of safe builtin container and scalar types.  Anything outside
# this set raises ``UnpicklingError``, which the deserialize loop already
# catches and turns into a skipped event, so the worst a hostile payload can do
# is be dropped -- never executed.  (Primitive payloads are reconstructed by
# dedicated pickle opcodes that never reach ``find_class``, so legitimate trace
# data is unaffected.)
_SAFE_PICKLE_GLOBALS: FrozenSet[Tuple[str, str]] = frozenset({
    ("builtins", "dict"),
    ("builtins", "list"),
    ("builtins", "tuple"),
    ("builtins", "set"),
    ("builtins", "frozenset"),
    ("builtins", "str"),
    ("builtins", "bytes"),
    ("builtins", "bytearray"),
    ("builtins", "int"),
    ("builtins", "float"),
    ("builtins", "complex"),
    ("builtins", "bool"),
    ("builtins", "NoneType"),
})


class _RestrictedUnpickler(pickle.Unpickler):
    """
        A :class:`pickle.Unpickler` that only permits a fixed allow-list of safe
        builtin container and scalar types.

        Used to deserialize trace payloads received over the network without
        exposing the server to pickle's arbitrary-object-construction (and
        therefore arbitrary-code-execution) behaviour.
    """

    def find_class(self, module: str, name: str) -> Any:
        """
            Override the global-resolution hook to reject any class that is not
            on the safe allow-list.

            :param module: The module the pickle stream is requesting an import from.
            :param name: The qualified name being requested from ``module``.

            :returns: The resolved class, when it is on the allow-list.
            :raises: pickle.UnpicklingError
        """
        requested = (module, name)
        if requested not in _SAFE_PICKLE_GLOBALS:
            err_msg_lines = ["Refusing to unpickle a disallowed global from an untrusted trace payload."]
            err_msg_lines.append("MODULE: {}".format(module))
            err_msg_lines.append("NAME: {}".format(name))

            err_msg = os.linesep.join(err_msg_lines)
            raise pickle.UnpicklingError(err_msg)

        rtnval = super().find_class(module, name)
        return rtnval


def _safe_pickle_loads(payload_data: bytes) -> Any:
    """
        Deserialize a trace payload using a restricted unpickler that only
        permits safe builtin container and scalar types.

        :param payload_data: The raw pickle bytes read from the stream.

        :returns: The deserialized payload object.
        :raises: pickle.UnpicklingError
    """
    buffer = io.BytesIO(payload_data)
    unpickler = _RestrictedUnpickler(buffer)
    rtnval = unpickler.load()
    return rtnval


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
                payload = _safe_pickle_loads(payload_data)
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
