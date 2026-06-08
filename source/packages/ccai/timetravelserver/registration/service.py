import datetime
import uuid
from typing import Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from ccai.timetravelserver.persistence.credential_store import CredentialStore
from ccai.timetravelserver.persistence.models import RegisteredProcess, PortalSnapshot

class UnauthorizedError(Exception):
    pass

class ProcessNotFoundError(Exception):
    pass

class RegistrationService:
    def __init__(self, session: Session, credential_store: CredentialStore):
        self._session = session
        self._credential_store = credential_store

    def register(
        self,
        credential_token: str,
        host: str,
        pid: int,
        application_name: str,
        pod_version: str,
        remote_control_address: str
    ) -> Tuple[str, str]:
        """
        Registers a new process or updates an existing one.
        Returns a tuple of (process_id, status).
        """
        cred = self._credential_store.validate(credential_token)
        if cred is None:
            raise UnauthorizedError("Invalid or revoked credential token")

        try:
            process = self._session.query(RegisteredProcess).filter_by(host=host, pid=pid).one()
            process.application_name = application_name
            process.pod_version = pod_version
            process.remote_control_address = remote_control_address
            process.lifecycle_state = "registered"
        except NoResultFound:
            process = RegisteredProcess(
                host=host,
                pid=pid,
                application_name=application_name,
                pod_version=pod_version,
                remote_control_address=remote_control_address,
                lifecycle_state="registered"
            )
            self._session.add(process)

        self._session.commit()
        return str(process.id), process.lifecycle_state

    def unregister(self, credential_token: str, process_id: str) -> Tuple[str, str]:
        """
        Unregisters an existing process.
        Returns a tuple of (process_id, status).
        """
        cred = self._credential_store.validate(credential_token)
        if cred is None:
            raise UnauthorizedError("Invalid or revoked credential token")

        try:
            process_uuid = uuid.UUID(process_id)
            process = self._session.query(RegisteredProcess).filter_by(id=process_uuid).one()
        except (ValueError, NoResultFound):
            raise ProcessNotFoundError("Process not found")

        # Create portal snapshot (we archive the state at unregistration)
        snapshot = PortalSnapshot(
            process_id=process.id,
            portal_name="unknown", # We don't have portal data in the request body for unregister according to specs
            is_active=False,
            snapshot_at=datetime.datetime.utcnow()
        )
        self._session.add(snapshot)

        process.lifecycle_state = "disconnected"
        process.disconnected_at = datetime.datetime.utcnow()

        self._session.commit()
        return str(process.id), process.lifecycle_state
