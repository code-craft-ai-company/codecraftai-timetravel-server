import uuid
import datetime
from dataclasses import dataclass
from typing import Callable, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from ccai.timetravelserver.persistence.models import RegisteredProcess, PortalSnapshot

# Abstracting CommandDispatcher until S2.5 is implemented
class CommandDispatcherError(Exception):
    pass

class CommandDispatcher:
    def dispatch(self, address: str, command: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        """Sends a command to a remote control address and returns the result."""
        raise NotImplementedError("To be implemented in S2.5")

@dataclass
class RefreshResult:
    success: bool
    updated_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class ProcessNotFoundError(Exception):
    pass

class MetadataRefreshService:
    def __init__(self, session_factory: Callable[[], Session], command_dispatcher: CommandDispatcher):
        self._session_factory = session_factory
        self._command_dispatcher = command_dispatcher

    def refresh(self, process_id: uuid.UUID) -> RefreshResult:
        session = self._session_factory()
        try:
            try:
                process = session.query(RegisteredProcess).filter_by(id=process_id).one()
            except NoResultFound:
                return RefreshResult(success=False, error_message="Process not found")

            if process.lifecycle_state in ["disconnected", "unreachable"]:
                return RefreshResult(success=False, error_message=f"Cannot refresh {process.lifecycle_state} process")

            try:
                # Query remote control
                portals = self._command_dispatcher.dispatch(process.remote_control_address, "list_portals")
                trace_config = self._command_dispatcher.dispatch(process.remote_control_address, "get_trace_config")

                # Note: Assuming portals is a list of dicts: [{"name": str, "is_active": bool}]
                # and trace_config is a dict

                # Delete old snapshots for active process refresh
                session.query(PortalSnapshot).filter_by(process_id=process.id).delete()

                # Add new snapshots
                for portal in portals:
                    snapshot = PortalSnapshot(
                        process_id=process.id,
                        portal_name=portal.get("name", "unknown"),
                        is_active=portal.get("is_active", False),
                        snapshot_at=datetime.datetime.utcnow()
                    )
                    session.add(snapshot)

                session.commit()

                return RefreshResult(
                    success=True,
                    updated_data={"portals": portals, "trace_config": trace_config}
                )

            except CommandDispatcherError as e:
                # Refresh failed due to connection error, but we don't change lifecycle_state here
                # HealthChecker handles the transition to unreachable
                session.rollback()
                return RefreshResult(success=False, error_message=str(e))
            except Exception as e:
                session.rollback()
                return RefreshResult(success=False, error_message=str(e))

        finally:
            session.close()
