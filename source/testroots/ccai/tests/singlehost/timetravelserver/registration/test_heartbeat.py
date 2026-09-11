"""
    .. module:: ccai.tests.singlehost.timetravelserver.registration.test_heartbeat
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the HeartbeatService and HealthChecker.
"""

import datetime
import uuid

import ccai.testbase as testbase

from ccai.testshared.assertions import assert_raises
from ccai.testshared.factories.timetravelserver.memorydatabase import MemoryDatabase, create_memory_database

from ccai.timetravelserver.persistence.credential_store import CredentialStore
from ccai.timetravelserver.persistence.models import RegisteredProcess
from ccai.timetravelserver.persistence.server_config_store import ServerConfigStore
from ccai.timetravelserver.registration.service import UnauthorizedError, ProcessNotFoundError
from ccai.timetravelserver.registration.heartbeat import HeartbeatService, HealthChecker


def create_test_process(session, state="registered", registered_at=None, last_heartbeat_at=None):
    process = RegisteredProcess(
        host="localhost",
        pid=1234,
        application_name="test_app",
        pod_version="1.0.0",
        remote_control_address="localhost:8080",
        lifecycle_state=state
    )
    if registered_at:
        process.registered_at = registered_at
    if last_heartbeat_at:
        process.last_heartbeat_at = last_heartbeat_at
    session.add(process)
    session.commit()
    return process


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_heartbeat_updates_timestamp_and_state(db: MemoryDatabase):
    db_session = db.session
    credential_store = CredentialStore(db_session)
    heartbeat_service = HeartbeatService(db_session, credential_store)

    _, token = credential_store.create("test_cred")
    process = create_test_process(db_session)

    assert process.last_heartbeat_at is None
    assert process.lifecycle_state == "registered"

    heartbeat_service.receive(credential_token=token, process_id=str(process.id))

    db_session.refresh(process)
    assert process.last_heartbeat_at is not None
    assert process.lifecycle_state == "active"


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_heartbeat_invalid_credentials(db: MemoryDatabase):
    credential_store = CredentialStore(db.session)
    heartbeat_service = HeartbeatService(db.session, credential_store)

    with assert_raises(UnauthorizedError):
        heartbeat_service.receive(credential_token="invalid", process_id=str(uuid.uuid4()))


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_heartbeat_unknown_process_id(db: MemoryDatabase):
    credential_store = CredentialStore(db.session)
    heartbeat_service = HeartbeatService(db.session, credential_store)

    _, token = credential_store.create("test_cred")
    with assert_raises(ProcessNotFoundError):
        heartbeat_service.receive(credential_token=token, process_id=str(uuid.uuid4()))


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_health_checker_transitions_active_to_stale(db: MemoryDatabase):
    db_session = db.session
    config_store = ServerConfigStore(db_session)
    checker = HealthChecker(db.session_factory, config_store)

    now = datetime.datetime.utcnow()
    timeout = config_store.get("heartbeat_timeout_seconds")
    last_hb = now - datetime.timedelta(seconds=timeout + 5)

    process = create_test_process(db_session, state="active", last_heartbeat_at=last_hb)

    checker.check_all()

    db_session.refresh(process)
    assert process.lifecycle_state == "stale"


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_health_checker_transitions_stale_to_unreachable(db: MemoryDatabase):
    db_session = db.session
    config_store = ServerConfigStore(db_session)
    checker = HealthChecker(db.session_factory, config_store)

    now = datetime.datetime.utcnow()
    timeout = config_store.get("heartbeat_timeout_seconds")
    last_hb = now - datetime.timedelta(seconds=(2 * timeout) + 5)

    process = create_test_process(db_session, state="stale", last_heartbeat_at=last_hb)

    checker.check_all()

    db_session.refresh(process)
    assert process.lifecycle_state == "unreachable"


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_health_checker_does_not_affect_recent_heartbeats(db: MemoryDatabase):
    db_session = db.session
    config_store = ServerConfigStore(db_session)
    checker = HealthChecker(db.session_factory, config_store)

    now = datetime.datetime.utcnow()
    timeout = config_store.get("heartbeat_timeout_seconds")
    last_hb = now - datetime.timedelta(seconds=timeout - 5)

    process = create_test_process(db_session, state="active", last_heartbeat_at=last_hb)

    checker.check_all()

    db_session.refresh(process)
    assert process.lifecycle_state == "active"


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
