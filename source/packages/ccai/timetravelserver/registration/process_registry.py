import uuid
from typing import Optional, List, Tuple, Dict, Callable
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from sqlalchemy.exc import NoResultFound

from ccai.timetravelserver.persistence.models import RegisteredProcess

class InvalidProcessStateError(Exception):
    pass

class ProcessRegistry:
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def list_processes(
        self,
        state: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: str = "registered_at",
        offset: int = 0,
        limit: int = 50
    ) -> Tuple[List[RegisteredProcess], int]:
        """Return paginated process list and total count."""
        session = self._session_factory()
        try:
            query = session.query(RegisteredProcess)

            if state:
                query = query.filter(RegisteredProcess.lifecycle_state == state)

            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    or_(
                        RegisteredProcess.application_name.ilike(search_term),
                        RegisteredProcess.host.ilike(search_term)
                    )
                )

            total_count = query.count()

            if hasattr(RegisteredProcess, sort_by):
                sort_col = getattr(RegisteredProcess, sort_by)
                query = query.order_by(sort_col.desc())
            else:
                query = query.order_by(RegisteredProcess.registered_at.desc())

            processes = query.offset(offset).limit(limit).all()
            return processes, total_count
        finally:
            session.close()

    def get_process(self, process_id: uuid.UUID) -> Optional[RegisteredProcess]:
        """Return a single process by ID."""
        session = self._session_factory()
        try:
            return session.query(RegisteredProcess).filter_by(id=process_id).one()
        except NoResultFound:
            return None
        finally:
            session.close()

    def delete_process(self, process_id: uuid.UUID) -> None:
        """Delete a disconnected process and its associated snapshots."""
        session = self._session_factory()
        try:
            try:
                process = session.query(RegisteredProcess).filter_by(id=process_id).one()
            except NoResultFound:
                return

            if process.lifecycle_state != "disconnected":
                raise InvalidProcessStateError("Can only delete processes in disconnected state")

            session.delete(process)
            session.commit()
        finally:
            session.close()

    def get_process_count_by_state(self) -> Dict[str, int]:
        """Return count of processes grouped by lifecycle_state."""
        session = self._session_factory()
        try:
            results = session.query(
                RegisteredProcess.lifecycle_state,
                func.count(RegisteredProcess.id)
            ).group_by(RegisteredProcess.lifecycle_state).all()

            return {state: count for state, count in results}
        finally:
            session.close()
