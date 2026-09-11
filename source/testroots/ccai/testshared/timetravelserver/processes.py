"""
    .. module:: ccai.testshared.timetravelserver.processes
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Helpers for seeding registered process rows in a test database.
"""

import uuid

from sqlalchemy.orm import sessionmaker
from typing import Optional

from ccai.timetravelserver.persistence.models import RegisteredProcess


def add_sample_process(session_factory: sessionmaker, *, application_name: str = "test-app", host: str = "localhost",
                       pid: int = 1234, pod_version: str = "1.0", lifecycle_state: str = "connected",
                       remote_control_address: Optional[str] = "127.0.0.1:9000") -> uuid.UUID:
    """
        Inserts a :class:`RegisteredProcess` row using a short-lived session from the
        given factory and returns its identifier.

        :param session_factory: The session factory bound to the test database.
        :param application_name: Application name recorded for the process.
        :param host: Host recorded for the process.
        :param pid: Process identifier recorded for the process.
        :param pod_version: Pod version recorded for the process.
        :param lifecycle_state: Lifecycle state recorded for the process.
        :param remote_control_address: Remote control address, or ``None`` to leave it unset.

        :returns: The UUID of the inserted process.
    """
    session = session_factory()
    try:
        process = RegisteredProcess(
            id=uuid.uuid4(),
            application_name=application_name,
            host=host,
            pid=pid,
            pod_version=pod_version,
            lifecycle_state=lifecycle_state,
            remote_control_address=remote_control_address
        )
        session.add(process)
        session.commit()
        process_id = process.id
    finally:
        session.close()

    return process_id
