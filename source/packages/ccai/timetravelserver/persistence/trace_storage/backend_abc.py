from typing import List
import datetime
from abc import ABC, abstractmethod

class TraceStorageBackend(ABC):
    @abstractmethod
    def write(self, data: bytes, session_id: str) -> str:
        """Writes initial data and returns a reference string."""
        pass

    @abstractmethod
    def append(self, reference: str, data: bytes) -> bool:
        """Appends bytes to the referenced storage."""
        pass

    @abstractmethod
    def finalize(self, reference: str) -> str:
        """Finalizes the storage (e.g., renames temp file to final) and returns new reference if changed."""
        pass

    @abstractmethod
    def read(self, reference: str) -> bytes:
        """Reads the entire finalized data."""
        pass

    @abstractmethod
    def list_references(self) -> List[str]:
        """Lists all finalized references."""
        pass

    @abstractmethod
    def delete(self, reference: str) -> bool:
        """Deletes the stored data."""
        pass

    @abstractmethod
    def exists(self, reference: str) -> bool:
        """Checks if a reference exists."""
        pass

    @abstractmethod
    def list_expired(self, cutoff_time: datetime.datetime) -> List[str]:
        """Returns references that were modified before cutoff_time."""
        pass
