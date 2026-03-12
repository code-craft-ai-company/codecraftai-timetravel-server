import threading
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class StreamRouter:
    def __init__(self, storage_backend_factory: Any, session_updater: Any = None):
        """
        :param storage_backend_factory: A callable that creates a new storage backend instance for a given session.
                                        Signature: (process_id: str, session_id: str) -> StorageBackend
        :param session_updater: An object/callable to update the database session record when finalized.
        """
        self._storage_factory = storage_backend_factory
        self._session_updater = session_updater

        # Maps (process_id, session_id) -> StorageBackend
        self._routing_table: Dict[tuple[str, str], Any] = {}
        self._lock = threading.Lock()

    def route_stream(self, process_id: str, session_id: str) -> Any:
        """
        Creates a storage reference for a new stream and registers it in the routing table.
        """
        key = (process_id, session_id)
        with self._lock:
            if key in self._routing_table:
                return self._routing_table[key]

            storage_backend = self._storage_factory(process_id, session_id)
            self._routing_table[key] = storage_backend
            return storage_backend

    def get_data_reference(self, process_id: str, session_id: str) -> Optional[Any]:
        """
        Looks up a storage reference from the routing table.
        """
        key = (process_id, session_id)
        with self._lock:
            return self._routing_table.get(key)

    def finalize_route(self, process_id: str, session_id: str, data_reference_uri: str) -> None:
        """
        Finalizes the storage and updates the session in the database.
        """
        key = (process_id, session_id)
        with self._lock:
            storage_backend = self._routing_table.pop(key, None)

        if storage_backend:
            try:
                storage_backend.commit()
            except Exception as e:
                logger.error(f"Failed to commit storage during finalize: {e}")

        if self._session_updater:
            try:
                self._session_updater.update_data_reference(session_id, data_reference_uri)
            except Exception as e:
                logger.error(f"Failed to update session with data reference: {e}")
