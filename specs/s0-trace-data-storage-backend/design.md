# S0.4 — Trace Data Storage Backend: Design

## Overview
An abstract storage interface with a filesystem implementation. Trace data is stored as binary files organized by process ID and session ID.

## Technical Architecture

### Module Layout
```
source/packages/ccai/timetravelserver/
    persistence/
        trace_storage/
            __init__.py
            backend_abc.py          # TraceStorageBackend ABC
            filesystem_backend.py   # FilesystemTraceStorage
```

### Abstract Interface

```python
class TraceStorageBackend(ABC):
    @abstractmethod
    def write(self, session_id: str, data: bytes) -> str:
        """Write data and return a data reference."""

    @abstractmethod
    def append(self, data_reference: str, data: bytes) -> None:
        """Append data to an existing stream."""

    @abstractmethod
    def finalize(self, data_reference: str) -> None:
        """Mark a stream as complete (atomic commit)."""

    @abstractmethod
    def read(self, data_reference: str) -> bytes:
        """Read all data for a reference."""

    @abstractmethod
    def list_references(self) -> List[str]:
        """List all stored data references."""

    @abstractmethod
    def delete(self, data_reference: str) -> None:
        """Delete stored data."""

    @abstractmethod
    def exists(self, data_reference: str) -> bool:
        """Check if a reference exists."""

    @abstractmethod
    def list_expired(self, max_age_days: int) -> List[str]:
        """List references older than max_age_days."""
```

### Filesystem Implementation

- **Base path**: Configured via S0.3 `trace_storage_path`.
- **Directory structure**: `{base_path}/{process_id}/{session_id}.trace`
- **Atomic writes**: Write to `{path}.tmp`, rename on `finalize()`.
- **Retention**: Use file modification time to determine age.

### Dependencies
- S0.3 (trace_storage_path, data_retention_days configuration)
- Python `os`, `shutil`, `pathlib` (stdlib)
