import uuid
from dataclasses import dataclass
from typing import Callable, List

from sqlalchemy.orm import Session

from ccai.timetravelserver.persistence.models import PortalSnapshot
from ccai.timetravelserver.registration.process_registry import ProcessRegistry
from ccai.timetravelserver.debugcontrol.command_dispatcher import CommandDispatcher

@dataclass
class PortalInfo:
    name: str
    is_active: bool

class PortalDiscoveryService:
    def __init__(self, session_factory: Callable[[], Session], command_dispatcher: CommandDispatcher, process_registry: ProcessRegistry):
        self._session_factory = session_factory
        self._command_dispatcher = command_dispatcher
        self._process_registry = process_registry

    def discover(self, process_id: uuid.UUID) -> List[PortalInfo]:
        """Query pod for portals and update local snapshots."""
        process = self._process_registry.get_process(process_id)
        if not process:
            raise ValueError(f"Process with ID {process_id} not found.")

        if not process.remote_control_address:
            raise ValueError(f"Process {process_id} has no remote control address.")

        response_data = self._command_dispatcher.dispatch(
            process.remote_control_address,
            "list_portals"
        )

        portals_data = response_data.get("portals", [])
        portal_infos = []
        for p in portals_data:
            portal_infos.append(PortalInfo(name=p.get("name"), is_active=p.get("is_active", False)))

        # Update local snapshots
        db_session = self._session_factory()
        try:
            # First, fetch existing snapshots to update or delete
            existing_snapshots = db_session.query(PortalSnapshot).filter_by(process_id=process_id).all()
            existing_map = {s.portal_name: s for s in existing_snapshots}

            for p_info in portal_infos:
                if p_info.name in existing_map:
                    # Update
                    snapshot = existing_map[p_info.name]
                    snapshot.is_active = p_info.is_active
                    del existing_map[p_info.name]
                else:
                    # Insert
                    snapshot = PortalSnapshot(
                        process_id=process_id,
                        portal_name=p_info.name,
                        is_active=p_info.is_active
                    )
                    db_session.add(snapshot)

            # Remaining in existing_map were not returned by pod, so delete them
            for s in existing_map.values():
                db_session.delete(s)

            db_session.commit()
        finally:
            db_session.close()

        return portal_infos
