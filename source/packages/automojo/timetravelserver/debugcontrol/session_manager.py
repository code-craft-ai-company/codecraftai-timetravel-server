import datetime
import uuid
from typing import Callable, List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from automojo.timetravelserver.persistence.models import TraceSession
from automojo.timetravelserver.registration.process_registry import ProcessRegistry


class DebugSessionManager:
    def __init__(self, session_factory: Callable[[], Session], process_registry: ProcessRegistry):
        self._session_factory = session_factory
        self._process_registry = process_registry

    def create_session(self, process_id: uuid.UUID, portal_names: List[str]) -> TraceSession:
        """Create a new active debug session."""
        # Verify process exists
        process = self._process_registry.get_process(process_id)
        if not process:
            raise ValueError(f"Process with ID {process_id} not found.")

        # Create session
        db_session = self._session_factory()
        try:
            trace_session = TraceSession(
                process_id=process_id,
                status="active"
            )
            # Future enhancement: we might want to store portal_names somewhere or they are
            # implied by the activation commands sent alongside this.
            db_session.add(trace_session)
            db_session.commit()
            db_session.refresh(trace_session)
            return trace_session
        finally:
            db_session.close()

    def close_session(self, session_id: uuid.UUID) -> TraceSession:
        """Close a session, set stopped_at and status=completed."""
        db_session = self._session_factory()
        try:
            trace_session = db_session.query(TraceSession).filter(TraceSession.id == session_id).one()
            trace_session.stopped_at = datetime.datetime.utcnow()
            trace_session.status = "completed"
            db_session.commit()
            db_session.refresh(trace_session)
            return trace_session
        except NoResultFound:
            raise ValueError(f"TraceSession with ID {session_id} not found.")
        finally:
            db_session.close()

    def list_sessions(self, process_id: Optional[uuid.UUID] = None,
                      status: Optional[str] = None) -> List[TraceSession]:
        """List sessions with optional filtering."""
        db_session = self._session_factory()
        try:
            query = db_session.query(TraceSession)
            if process_id:
                query = query.filter(TraceSession.process_id == process_id)
            if status:
                query = query.filter(TraceSession.status == status)

            return query.order_by(TraceSession.started_at.desc()).all()
        finally:
            db_session.close()

    def get_session(self, session_id: uuid.UUID) -> Optional[TraceSession]:
        """Get session detail."""
        db_session = self._session_factory()
        try:
            return db_session.query(TraceSession).filter(TraceSession.id == session_id).one_or_none()
        finally:
            db_session.close()

    def update_data_reference(self, session_id: uuid.UUID, data_reference: str) -> None:
        """Link trace data storage reference to session."""
        db_session = self._session_factory()
        try:
            trace_session = db_session.query(TraceSession).filter(TraceSession.id == session_id).one()
            trace_session.data_reference = data_reference
            db_session.commit()
        except NoResultFound:
            raise ValueError(f"TraceSession with ID {session_id} not found.")
        finally:
            db_session.close()
