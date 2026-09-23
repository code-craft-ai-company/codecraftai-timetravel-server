import uuid
from typing import Callable, Dict, List

from sqlalchemy.orm import Session

from ccai.timetravelserver.persistence.models import PortalSnapshot
from ccai.timetravelserver.registration.process_registry import ProcessRegistry
from ccai.timetravelserver.debugcontrol.command_dispatcher import CommandDispatcher

class PortalControlService:
    def __init__(self, session_factory: Callable[[], Session], command_dispatcher: CommandDispatcher, process_registry: ProcessRegistry):
        self._session_factory = session_factory
        self._command_dispatcher = command_dispatcher
        self._process_registry = process_registry

    def _update_snapshot(self, process_id: uuid.UUID, portal_name: str, is_active: bool) -> None:
        db_session = self._session_factory()
        try:
            snapshot = db_session.query(PortalSnapshot).filter_by(
                process_id=process_id, portal_name=portal_name
            ).one_or_none()

            if snapshot:
                snapshot.is_active = is_active
            else:
                snapshot = PortalSnapshot(
                    process_id=process_id,
                    portal_name=portal_name,
                    is_active=is_active
                )
                db_session.add(snapshot)
            db_session.commit()
        finally:
            db_session.close()

    def activate_portal(self, process_id: uuid.UUID, portal_name: str) -> bool:
        """Activate a single portal. Returns True on success."""
        process = self._process_registry.get_process(process_id)
        if not process:
            raise ValueError(f"Process with ID {process_id} not found.")
        if not process.remote_control_address:
            raise ValueError(f"Process {process_id} has no remote control address.")

        response = self._command_dispatcher.dispatch(
            process.remote_control_address,
            "activate_portal",
            {"portal_name": portal_name}
        )

        success = response.get("success", False)
        if success:
            self._update_snapshot(process_id, portal_name, True)
        return success

    def deactivate_portal(self, process_id: uuid.UUID, portal_name: str) -> bool:
        """Deactivate a single portal. Returns True on success."""
        process = self._process_registry.get_process(process_id)
        if not process:
            raise ValueError(f"Process with ID {process_id} not found.")
        if not process.remote_control_address:
            raise ValueError(f"Process {process_id} has no remote control address.")

        response = self._command_dispatcher.dispatch(
            process.remote_control_address,
            "deactivate_portal",
            {"portal_name": portal_name}
        )

        success = response.get("success", False)
        if success:
            self._update_snapshot(process_id, portal_name, False)
        return success

    def activate_portals(self, process_id: uuid.UUID, portal_names: List[str]) -> Dict[str, bool]:
        """Bulk activate. Returns {name: success} map."""
        results = {}
        for name in portal_names:
            try:
                success = self.activate_portal(process_id, name)
                results[name] = success
            except Exception:
                results[name] = False
        return results

    def deactivate_portals(self, process_id: uuid.UUID, portal_names: List[str]) -> Dict[str, bool]:
        """Bulk deactivate. Returns {name: success} map."""
        results = {}
        for name in portal_names:
            try:
                success = self.deactivate_portal(process_id, name)
                results[name] = success
            except Exception:
                results[name] = False
        return results
