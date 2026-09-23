"""
    .. module:: ccai.tests.singlehost.timetravelserver.streamreceiver.test_deserializer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the HybridFormatDeserializer and the restricted unpickler.
"""

import io
import struct
import pickle
import tempfile

from ccai.testshared.assertions import assert_raises

from ccai.timetravelserver.streamreceiver.deserializer import HybridFormatDeserializer
from ccai.timetravelserver.streamreceiver.deserializer import _safe_pickle_loads
from ccai.timetravelserver.tracedata.events import EventType, CallEvent, ReturnEvent, LineEvent


class _PickleGadget:
    """
        A pickle payload that, under a stock ``pickle.loads``, would resolve and
        call ``eval`` -- i.e. a real remote-code-execution gadget.  Used to prove
        the restricted unpickler refuses non-allow-listed globals.
    """

    def __reduce__(self):
        rtnval = (eval, ("1 + 1",))
        return rtnval

def pack_event(event_type: EventType, timestamp: float, payload: dict) -> bytes:
    type_str = event_type.value.encode('utf-8')
    type_len = len(type_str)

    payload_data = pickle.dumps(payload)

    header = struct.pack("!B", type_len) + type_str + struct.pack("!d I", timestamp, len(payload_data))
    return header + payload_data

def test_deserializer_call_event():
    deserializer = HybridFormatDeserializer()
    stream = io.BytesIO()

    event_type = EventType.CALL
    timestamp = 1000.5
    payload = {
        "function_name": "test_func",
        "file_name": "test_file.py",
        "line_number": 10,
        "arguments": {"a": 1}
    }

    stream.write(pack_event(event_type, timestamp, payload))
    stream.seek(0)

    events = list(deserializer.deserialize_stream(stream, "proc1", "sess1", "port1"))

    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CallEvent)
    assert event.event_type == EventType.CALL
    assert event.timestamp == timestamp
    assert event.process_id == "proc1"
    assert event.session_id == "sess1"
    assert event.portal_name == "port1"
    assert event.function_name == "test_func"
    assert event.file_name == "test_file.py"
    assert event.line_number == 10
    assert event.arguments == {"a": 1}

def test_deserializer_return_event():
    deserializer = HybridFormatDeserializer()
    stream = io.BytesIO()

    event_type = EventType.RETURN
    timestamp = 1001.0
    payload = {
        "function_name": "test_func",
        "file_name": "test_file.py",
        "line_number": 15,
        "return_value": 42
    }

    stream.write(pack_event(event_type, timestamp, payload))
    stream.seek(0)

    events = list(deserializer.deserialize_stream(stream, "proc1", "sess1", "port1"))

    assert len(events) == 1
    event = events[0]
    assert isinstance(event, ReturnEvent)
    assert event.event_type == EventType.RETURN
    assert event.timestamp == timestamp
    assert event.function_name == "test_func"
    assert event.return_value == 42

def test_deserializer_line_event():
    deserializer = HybridFormatDeserializer()
    stream = io.BytesIO()

    event_type = EventType.LINE
    timestamp = 1003.0
    payload = {
        "file_name": "test.py",
        "function_name": "test_func",
        "line_number": 20,
        "locals_snapshot": {"b": 2}
    }

    stream.write(pack_event(event_type, timestamp, payload))
    stream.seek(0)

    events = list(deserializer.deserialize_stream(stream, "proc1", "sess1", "port1"))

    assert len(events) == 1
    event = events[0]
    assert isinstance(event, LineEvent)
    assert event.event_type == EventType.LINE
    assert event.timestamp == timestamp
    assert event.file_name == "test.py"
    assert event.line_number == 20
    assert event.locals_snapshot == {"b": 2}

def test_deserializer_incremental_stream():
    deserializer = HybridFormatDeserializer()
    stream = io.BytesIO()

    payload_1 = {"function_name": "f1", "file_name": "f.py", "line_number": 1, "arguments": {}}
    payload_2 = {"function_name": "f1", "file_name": "f.py", "line_number": 2, "return_value": 1}

    stream.write(pack_event(EventType.CALL, 1000.0, payload_1))
    stream.write(pack_event(EventType.RETURN, 1001.0, payload_2))
    stream.seek(0)

    events = list(deserializer.deserialize_stream(stream, "p1", "s1", "port1"))
    assert len(events) == 2
    assert isinstance(events[0], CallEvent)
    assert isinstance(events[1], ReturnEvent)

def test_deserializer_corrupted_payload_skipped():
    deserializer = HybridFormatDeserializer()
    stream = io.BytesIO()

    payload_1 = {"function_name": "f1", "file_name": "f.py", "line_number": 1, "arguments": {}}
    stream.write(pack_event(EventType.CALL, 1000.0, payload_1))

    # Event 2: Corrupted Payload
    type_str = EventType.RETURN.value.encode('utf-8')
    type_len = len(type_str)
    bad_payload = b"corrupted pickle data"
    env_2 = struct.pack("!B", type_len) + type_str + struct.pack("!d I", 1001.0, len(bad_payload))
    stream.write(env_2 + bad_payload)

    payload_3 = {"function_name": "f2", "file_name": "f.py", "line_number": 1, "arguments": {}}
    stream.write(pack_event(EventType.CALL, 1002.0, payload_3))

    stream.seek(0)

    events = list(deserializer.deserialize_stream(stream, "p1", "s1", "port1"))

    # Should get events 1 and 3, skip 2
    assert len(events) == 2
    assert events[0].function_name == "f1"
    assert events[1].function_name == "f2"

def test_deserializer_corrupted_envelope_detected():
    deserializer = HybridFormatDeserializer()
    stream = io.BytesIO()

    # Write bad envelope
    stream.write(b'\x05') # type len 5
    stream.write(b'BADTY') # Invalid type
    stream.write(struct.pack("!d I", 1000.0, 10))
    stream.write(b"0123456789")
    stream.seek(0)

    events = list(deserializer.deserialize_stream(stream, "p1", "s1", "port1"))

    assert len(events) == 0

def test_safe_pickle_loads_rejects_disallowed_global():
    # A reduce gadget that targets ``eval`` (not on the safe allow-list) must be
    # refused before the callable is ever invoked.
    gadget_bytes = pickle.dumps(_PickleGadget())

    with assert_raises(pickle.UnpicklingError):
        _safe_pickle_loads(gadget_bytes)


def test_safe_pickle_loads_allows_primitive_payload():
    # Legitimate primitive trace payloads must still round-trip unchanged.
    payload = {"function_name": "f", "line_number": 3, "arguments": {"a": 1}, "tags": ["x", "y"]}
    payload_bytes = pickle.dumps(payload)

    result = _safe_pickle_loads(payload_bytes)

    assert result == payload


def test_deserializer_skips_malicious_pickle_gadget():
    # An RCE gadget embedded in the stream must be skipped (never executed) and
    # the deserializer must continue on to the next, legitimate event.
    deserializer = HybridFormatDeserializer()
    stream = io.BytesIO()

    gadget_bytes = pickle.dumps(_PickleGadget())
    type_str = EventType.CALL.value.encode('utf-8')
    bad_env = struct.pack("!B", len(type_str)) + type_str + struct.pack("!d I", 1000.0, len(gadget_bytes))
    stream.write(bad_env + gadget_bytes)

    good_payload = {"function_name": "safe_func", "file_name": "f.py", "line_number": 1, "arguments": {}}
    stream.write(pack_event(EventType.CALL, 1001.0, good_payload))
    stream.seek(0)

    events = list(deserializer.deserialize_stream(stream, "p1", "s1", "port1"))

    assert len(events) == 1
    assert events[0].function_name == "safe_func"


def test_deserializer_round_trip():
    deserializer = HybridFormatDeserializer()

    events_to_write = [
        (EventType.CALL, 1.0, {"function_name": "f", "file_name": "f.py", "line_number": 1, "arguments": {}}),
        (EventType.RETURN, 2.0, {"function_name": "f", "file_name": "f.py", "line_number": 2, "return_value": 42})
    ]

    with tempfile.TemporaryFile() as f:
        for ev in events_to_write:
            f.write(pack_event(ev[0], ev[1], ev[2]))

        f.seek(0)

        events = list(deserializer.deserialize_stream(f, "p1", "s1", "port1"))

        assert len(events) == 2
        assert isinstance(events[0], CallEvent)
        assert isinstance(events[1], ReturnEvent)
        assert events[0].function_name == "f"
        assert events[1].return_value == 42


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
