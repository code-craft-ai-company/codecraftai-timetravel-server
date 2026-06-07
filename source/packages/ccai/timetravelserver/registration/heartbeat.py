import datetime
import uuid
import threading
from typing import Callable
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from ccai.timetravelserver.persistence.credential_store import CredentialStore
from ccai.timetravelserver.persistence.models import RegisteredProcess
from ccai.timetravelserver.persistence.server_config_store import ServerConfigStore
from ccai.timetravelserver.registration.service import UnauthorizedError, ProcessNotFoundError

class HeartbeatService:
    def __init__(self, session: Session, credential_store: CredentialStore):
        self._session = session
        self._credential_store = credential_store

    def receive(self, credential_token: str, process_id: str) -> None:
        """
        Receives a heartbeat, validates credentials, and updates the process state and timestamp.
        """
        cred = self._credential_store.validate(credential_token)
        if cred is None:
            raise UnauthorizedError("Invalid or revoked credential token")

        try:
            process_uuid = uuid.UUID(process_id)
            process = self._session.query(RegisteredProcess).filter_by(id=process_uuid).one()
        except (ValueError, NoResultFound):
            raise ProcessNotFoundError("Process not found")

        process.last_heartbeat_at = datetime.datetime.utcnow()
        process.lifecycle_state = "active"

        self._session.commit()

class HealthChecker:
    def __init__(self, session_factory: Callable[[], Session], config_store: ServerConfigStore):
        self._session_factory = session_factory
        self._config_store = config_store
        self._timer = None

    def start(self) -> None:
        """Starts the background health check scheduling."""
        self._schedule_next()

    def stop(self) -> None:
        """Stops the background health check scheduling."""
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def _schedule_next(self) -> None:
        timeout = self._config_store.get("heartbeat_timeout_seconds")
        # Run check every half-timeout
        interval = max(1, timeout / 2)
        self._timer = threading.Timer(interval, self._run_and_reschedule)
        self._timer.daemon = True
        self._timer.start()

    def _run_and_reschedule(self) -> None:
        try:
            self.check_all()
        finally:
            self._schedule_next()

    def check_all(self) -> None:
        """Scan all active/stale processes and apply state transitions based on last_heartbeat_at."""
        session = self._session_factory()
        try:
            timeout_seconds = self._config_store.get("heartbeat_timeout_seconds")
            now = datetime.datetime.utcnow()

            stale_threshold = now - datetime.timedelta(seconds=timeout_seconds)
            unreachable_threshold = now - datetime.timedelta(seconds=2 * timeout_seconds)

            # Active -> Stale
            active_processes = session.query(RegisteredProcess).filter_by(lifecycle_state="active").all()
            for process in active_processes:
                if process.last_heartbeat_at and process.last_heartbeat_at < stale_threshold:
                    process.lifecycle_state = "stale"

            # Stale -> Unreachable
            stale_processes = session.query(RegisteredProcess).filter_by(lifecycle_state="stale").all()
            for process in stale_processes:
                if process.last_heartbeat_at and process.last_heartbeat_at < unreachable_threshold:
                    process.lifecycle_state = "unreachable"
                # Some processes might not have last_heartbeat_at if they were manually set to stale, or were just registered and never heartbeated but state somehow was stale
                elif not process.last_heartbeat_at and process.registered_at < unreachable_threshold:
                    process.lifecycle_state = "unreachable"

            # Registered -> Stale -> Unreachable (Handling edge cases where heartbeat never arrived)
            registered_processes = session.query(RegisteredProcess).filter_by(lifecycle_state="registered").all()
            for process in registered_processes:
                if process.registered_at < unreachable_threshold:
                    process.lifecycle_state = "unreachable"
                elif process.registered_at < stale_threshold:
                    process.lifecycle_state = "stale"

            session.commit()
        finally:
            session.close()
