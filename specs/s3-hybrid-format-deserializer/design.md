# S3.3 — Hybrid Format Deserializer: Design

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    streamreceiver/
        deserializer.py   # HybridFormatDeserializer
```

### Envelope Format (struct)
```
Format string: "!BdQHIQ"
B  - event_type     (uint8,  1 byte)
d  - timestamp      (float64, 8 bytes)
Q  - thread_id      (uint64, 8 bytes)
H  - filename_len   (uint16, 2 bytes)
I  - line_number    (uint32, 4 bytes)
Q  - payload_length (uint64, 8 bytes)
Total envelope: 31 bytes
```

### Class: HybridFormatDeserializer

```python
class HybridFormatDeserializer:
    ENVELOPE_SIZE = struct.calcsize("!BdQHIQ")

    def __init__(self, process_id: UUID, session_id: UUID):
        ...

    def deserialize_stream(self, stream: IO[bytes]) -> Iterator[TraceEvent]:
        """Yield TraceEvent objects from a binary stream."""

    def _parse_envelope(self, data: bytes) -> dict:
        """Parse envelope fields from bytes."""

    def _materialize_event(self, envelope: dict, filename: str, payload: Any) -> TraceEvent:
        """Construct the appropriate TraceEvent subclass."""
```

### Dependencies
- S0.5 (TraceEvent subclasses)
- Python `struct`, `pickle`, `io` (stdlib)
