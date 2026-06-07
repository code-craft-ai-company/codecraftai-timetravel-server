import pytest
import datetime
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ccai.timetravelserver.persistence.models.base import Base
from ccai.timetravelserver.persistence.credential_store import CredentialStore
from ccai.timetravelserver.persistence.models import RegisteredProcess, ServerConfiguration
from ccai.timetravelserver.persistence.server_config_store import ServerConfigStore
from ccai.timetravelserver.registration.service import UnauthorizedError, ProcessNotFoundError
from ccai.timetravelserver.registration.heartbeat import HeartbeatService, HealthChecker

@pytest.fixture
def db_engine():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def db_session_factory(db_engine):
    return sessionmaker(bind=db_engine)

@pytest.fixture
def db_session(db_session_factory):
    session = db_session_factory()
    yield session
    session.close()

@pytest.fixture
def credential_store(db_session):
    return CredentialStore(db_session)

@pytest.fixture
def config_store(db_session):
    return ServerConfigStore(db_session)

@pytest.fixture
def heartbeat_service(db_session, credential_store):
    return HeartbeatService(db_session, credential_store)

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

def test_heartbeat_updates_timestamp_and_state(db_session, credential_store, heartbeat_service):
    _, token = credential_store.create("test_cred")
    process = create_test_process(db_session)

    assert process.last_heartbeat_at is None
    assert process.lifecycle_state == "registered"

    heartbeat_service.receive(credential_token=token, process_id=str(process.id))

    db_session.refresh(process)
    assert process.last_heartbeat_at is not None
    assert process.lifecycle_state == "active"

def test_heartbeat_invalid_credentials(heartbeat_service):
    with pytest.raises(UnauthorizedError):
        heartbeat_service.receive(credential_token="invalid", process_id=str(uuid.uuid4()))

def test_heartbeat_unknown_process_id(credential_store, heartbeat_service):
    _, token = credential_store.create("test_cred")
    with pytest.raises(ProcessNotFoundError):
        heartbeat_service.receive(credential_token=token, process_id=str(uuid.uuid4()))

def test_health_checker_transitions_active_to_stale(db_session_factory, db_session, config_store):
    checker = HealthChecker(db_session_factory, config_store)

    now = datetime.datetime.utcnow()
    timeout = config_store.get("heartbeat_timeout_seconds")
    last_hb = now - datetime.timedelta(seconds=timeout + 5)

    process = create_test_process(db_session, state="active", last_heartbeat_at=last_hb)

    checker.check_all()

    db_session.refresh(process)
    assert process.lifecycle_state == "stale"

def test_health_checker_transitions_stale_to_unreachable(db_session_factory, db_session, config_store):
    checker = HealthChecker(db_session_factory, config_store)

    now = datetime.datetime.utcnow()
    timeout = config_store.get("heartbeat_timeout_seconds")
    last_hb = now - datetime.timedelta(seconds=(2 * timeout) + 5)

    process = create_test_process(db_session, state="stale", last_heartbeat_at=last_hb)

    checker.check_all()

    db_session.refresh(process)
    assert process.lifecycle_state == "unreachable"

def test_health_checker_does_not_affect_recent_heartbeats(db_session_factory, db_session, config_store):
    checker = HealthChecker(db_session_factory, config_store)

    now = datetime.datetime.utcnow()
    timeout = config_store.get("heartbeat_timeout_seconds")
    last_hb = now - datetime.timedelta(seconds=timeout - 5)

    process = create_test_process(db_session, state="active", last_heartbeat_at=last_hb)

    checker.check_all()

    db_session.refresh(process)
    assert process.lifecycle_state == "active"
