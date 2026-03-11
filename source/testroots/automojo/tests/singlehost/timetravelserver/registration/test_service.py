import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from automojo.timetravelserver.persistence.models.base import Base
from automojo.timetravelserver.persistence.credential_store import CredentialStore
from automojo.timetravelserver.persistence.models import RegisteredProcess
from automojo.timetravelserver.registration.service import RegistrationService, UnauthorizedError, ProcessNotFoundError
from automojo.timetravelserver.persistence.models import PortalSnapshot
import uuid

@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def credential_store(db_session):
    return CredentialStore(db_session)

@pytest.fixture
def registration_service(db_session, credential_store):
    return RegistrationService(db_session, credential_store)

def test_successful_registration(db_session, credential_store, registration_service):
    _, token = credential_store.create("test_cred")

    process_id, status = registration_service.register(
        credential_token=token,
        host="localhost",
        pid=1234,
        application_name="test_app",
        pod_version="1.0.0",
        remote_control_address="localhost:8080"
    )

    assert status == "registered"
    assert process_id is not None

    import uuid
    process = db_session.query(RegisteredProcess).filter_by(id=uuid.UUID(process_id)).one()
    assert process.host == "localhost"
    assert process.pid == 1234
    assert process.application_name == "test_app"
    assert process.pod_version == "1.0.0"
    assert process.remote_control_address == "localhost:8080"

def test_registration_rejected_with_invalid_credentials(registration_service):
    with pytest.raises(UnauthorizedError):
        registration_service.register(
            credential_token="invalid_token",
            host="localhost",
            pid=1234,
            application_name="test_app",
            pod_version="1.0.0",
            remote_control_address="localhost:8080"
        )

def test_registration_rejected_with_revoked_credentials(credential_store, registration_service):
    cred, token = credential_store.create("test_cred")
    credential_store.revoke(str(cred.id))

    with pytest.raises(UnauthorizedError):
        registration_service.register(
            credential_token=token,
            host="localhost",
            pid=1234,
            application_name="test_app",
            pod_version="1.0.0",
            remote_control_address="localhost:8080"
        )

def test_duplicate_host_pid_updates_existing_record(db_session, credential_store, registration_service):
    _, token = credential_store.create("test_cred")

    process_id1, _ = registration_service.register(
        credential_token=token,
        host="localhost",
        pid=1234,
        application_name="test_app",
        pod_version="1.0.0",
        remote_control_address="localhost:8080"
    )

    process_id2, _ = registration_service.register(
        credential_token=token,
        host="localhost",
        pid=1234,
        application_name="new_app",
        pod_version="1.0.1",
        remote_control_address="localhost:8081"
    )

    assert process_id1 == process_id2

    import uuid
    process = db_session.query(RegisteredProcess).filter_by(id=uuid.UUID(process_id1)).one()
    assert process.application_name == "new_app"
    assert process.pod_version == "1.0.1"
    assert process.remote_control_address == "localhost:8081"

def test_successful_unregistration(db_session, credential_store, registration_service):
    _, token = credential_store.create("test_cred")

    process_id, _ = registration_service.register(
        credential_token=token,
        host="localhost",
        pid=1234,
        application_name="test_app",
        pod_version="1.0.0",
        remote_control_address="localhost:8080"
    )

    unreg_process_id, status = registration_service.unregister(
        credential_token=token,
        process_id=process_id
    )

    assert unreg_process_id == process_id
    assert status == "disconnected"

    process = db_session.query(RegisteredProcess).filter_by(id=uuid.UUID(process_id)).one()
    assert process.lifecycle_state == "disconnected"
    assert process.disconnected_at is not None

def test_unregistration_creates_portal_snapshots(db_session, credential_store, registration_service):
    _, token = credential_store.create("test_cred")

    process_id, _ = registration_service.register(
        credential_token=token,
        host="localhost",
        pid=1234,
        application_name="test_app",
        pod_version="1.0.0",
        remote_control_address="localhost:8080"
    )

    registration_service.unregister(
        credential_token=token,
        process_id=process_id
    )

    snapshots = db_session.query(PortalSnapshot).filter_by(process_id=uuid.UUID(process_id)).all()
    assert len(snapshots) > 0

def test_unregistration_rejected_with_invalid_credentials(registration_service):
    with pytest.raises(UnauthorizedError):
        registration_service.unregister(
            credential_token="invalid_token",
            process_id=str(uuid.uuid4())
        )

def test_unregistration_rejected_with_unknown_process_id(credential_store, registration_service):
    _, token = credential_store.create("test_cred")

    with pytest.raises(ProcessNotFoundError):
        registration_service.unregister(
            credential_token=token,
            process_id=str(uuid.uuid4())
        )
