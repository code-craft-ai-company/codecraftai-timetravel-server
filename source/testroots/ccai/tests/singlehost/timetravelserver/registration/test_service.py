"""
    .. module:: ccai.tests.singlehost.timetravelserver.registration.test_service
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the RegistrationService.
"""

import uuid

import ccai.testbase as testbase

from ccai.testshared.assertions import assert_raises
from ccai.testshared.factories.timetravelserver.memorydatabase import MemoryDatabase, create_memory_database

from ccai.timetravelserver.persistence.credential_store import CredentialStore
from ccai.timetravelserver.persistence.models import RegisteredProcess
from ccai.timetravelserver.persistence.models import PortalSnapshot
from ccai.timetravelserver.registration.service import RegistrationService, UnauthorizedError, ProcessNotFoundError


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_successful_registration(db: MemoryDatabase):
    db_session = db.session
    credential_store = CredentialStore(db_session)
    registration_service = RegistrationService(db_session, credential_store)

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

    process = db_session.query(RegisteredProcess).filter_by(id=uuid.UUID(process_id)).one()
    assert process.host == "localhost"
    assert process.pid == 1234
    assert process.application_name == "test_app"
    assert process.pod_version == "1.0.0"
    assert process.remote_control_address == "localhost:8080"


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_registration_rejected_with_invalid_credentials(db: MemoryDatabase):
    credential_store = CredentialStore(db.session)
    registration_service = RegistrationService(db.session, credential_store)

    with assert_raises(UnauthorizedError):
        registration_service.register(
            credential_token="invalid_token",
            host="localhost",
            pid=1234,
            application_name="test_app",
            pod_version="1.0.0",
            remote_control_address="localhost:8080"
        )


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_registration_rejected_with_revoked_credentials(db: MemoryDatabase):
    credential_store = CredentialStore(db.session)
    registration_service = RegistrationService(db.session, credential_store)

    cred, token = credential_store.create("test_cred")
    credential_store.revoke(str(cred.id))

    with assert_raises(UnauthorizedError):
        registration_service.register(
            credential_token=token,
            host="localhost",
            pid=1234,
            application_name="test_app",
            pod_version="1.0.0",
            remote_control_address="localhost:8080"
        )


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_duplicate_host_pid_updates_existing_record(db: MemoryDatabase):
    db_session = db.session
    credential_store = CredentialStore(db_session)
    registration_service = RegistrationService(db_session, credential_store)

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

    process = db_session.query(RegisteredProcess).filter_by(id=uuid.UUID(process_id1)).one()
    assert process.application_name == "new_app"
    assert process.pod_version == "1.0.1"
    assert process.remote_control_address == "localhost:8081"


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_successful_unregistration(db: MemoryDatabase):
    db_session = db.session
    credential_store = CredentialStore(db_session)
    registration_service = RegistrationService(db_session, credential_store)

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


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_unregistration_creates_portal_snapshots(db: MemoryDatabase):
    db_session = db.session
    credential_store = CredentialStore(db_session)
    registration_service = RegistrationService(db_session, credential_store)

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


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_unregistration_rejected_with_invalid_credentials(db: MemoryDatabase):
    credential_store = CredentialStore(db.session)
    registration_service = RegistrationService(db.session, credential_store)

    with assert_raises(UnauthorizedError):
        registration_service.unregister(
            credential_token="invalid_token",
            process_id=str(uuid.uuid4())
        )


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_unregistration_rejected_with_unknown_process_id(db: MemoryDatabase):
    credential_store = CredentialStore(db.session)
    registration_service = RegistrationService(db.session, credential_store)

    _, token = credential_store.create("test_cred")

    with assert_raises(ProcessNotFoundError):
        registration_service.unregister(
            credential_token=token,
            process_id=str(uuid.uuid4())
        )


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
