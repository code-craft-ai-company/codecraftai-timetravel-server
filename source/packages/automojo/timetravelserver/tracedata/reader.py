import logging
import os
from typing import BinaryIO, Iterator, Union

from automojo.timetravelserver.tracedata.events import TraceEvent
from automojo.timetravelserver.streamreceiver.deserializer import HybridFormatDeserializer

logger = logging.getLogger(__name__)

class TraceFileReader:
    """Reads a saved trace data file, yielding TraceEvent objects."""

    def __init__(self, process_id: str = "unknown", session_id: str = "unknown", portal_name: str = "unknown"):
        self.process_id = process_id
        self.session_id = session_id
        self.portal_name = portal_name
        self.deserializer = HybridFormatDeserializer()

    def read_events(self, source: Union[str, os.PathLike, BinaryIO]) -> Iterator[TraceEvent]:
        """
        Reads events from a file path or a binary stream.
        Loads data incrementally and delegates to HybridFormatDeserializer.
        """
        if hasattr(source, "read"):
            # It's a file-like object
            yield from self.deserializer.deserialize_stream(
                source,
                self.process_id,
                self.session_id,
                self.portal_name
            )
        else:
            # It's a file path
            if not os.path.exists(source):
                raise FileNotFoundError(f"Trace data file not found: {source}")

            with open(source, "rb") as f:
                yield from self.deserializer.deserialize_stream(
                    f,
                    self.process_id,
                    self.session_id,
                    self.portal_name
                )
