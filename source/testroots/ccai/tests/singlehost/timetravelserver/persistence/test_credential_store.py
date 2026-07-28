"""
    .. module:: ccai.tests.singlehost.timetravelserver.persistence.test_credential_store
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the CredentialStore.
"""

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import ccai.testbase as testbase

from ccai.timetravelserver.persistence.models import Base
from ccai.timetravelserver.persistence.credential_store import CredentialStore

from typing import Generator

@testbase.register.resource_factory()
def credstore_db_session() -> Generator[Session, None, None]:
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(bind=engine)
    session = SessionFactory()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


@testbase.attach.parameter(credstore_db_session, identifier='db_session')
def test_credential_creation(db_session: Session):
    store = CredentialStore(db_session)
    cred, plain_token = store.create("my-app", expires_in_days=30)

    testbase.assert_true(len(plain_token) > 20)
    testbase.assert_equal(cred.label, "my-app")
    testbase.assert_true(cred.expires_at is not None)

@testbase.attach.parameter(credstore_db_session, identifier='db_session')
def test_credential_validation_success(db_session: Session):
    store = CredentialStore(db_session)
    cred, plain_token = store.create("my-app")

    validated_cred = store.validate(plain_token)
    testbase.assert_true(validated_cred is not None)
    testbase.assert_equal(validated_cred.id, cred.id)
    testbase.assert_true(validated_cred.last_used_at is not None)

@testbase.attach.parameter(credstore_db_session, identifier='db_session')
def test_credential_validation_failure(db_session: Session):
    store = CredentialStore(db_session)
    store.create("my-app")

    validated_cred = store.validate("invalid_token")
    testbase.assert_true(validated_cred is None)

@testbase.attach.parameter(credstore_db_session, identifier='db_session')
def test_credential_revocation(db_session: Session):
    store = CredentialStore(db_session)
    cred, plain_token = store.create("my-app")

    testbase.assert_true(store.revoke(str(cred.id)))

    validated_cred = store.validate(plain_token)
    testbase.assert_true(validated_cred is None)

@testbase.attach.parameter(credstore_db_session, identifier='db_session')
def test_credential_expiration(db_session: Session):
    store = CredentialStore(db_session)
    cred, plain_token = store.create("my-app", expires_in_days=-1) # Expired 1 day ago

    validated_cred = store.validate(plain_token)
    testbase.assert_true(validated_cred is None)

@testbase.attach.parameter(credstore_db_session, identifier='db_session')
def test_credential_rotation(db_session: Session):
    store = CredentialStore(db_session)
    cred, old_token = store.create("my-app")

    new_cred_tuple = store.rotate(str(cred.id))
    testbase.assert_true(new_cred_tuple is not None)
    new_cred, new_token = new_cred_tuple

    # Old token invalid
    testbase.assert_true(store.validate(old_token) is None)

    # New token valid
    validated_cred = store.validate(new_token)
    testbase.assert_true(validated_cred is not None)
    testbase.assert_equal(validated_cred.label, "my-app")

@testbase.attach.parameter(credstore_db_session, identifier='db_session')
def test_list_credentials(db_session: Session):
    # Clear any existing credentials before testing
    from ccai.timetravelserver.persistence.models import Credential
    db_session.query(Credential).delete()
    db_session.commit()

    store = CredentialStore(db_session)
    store.create("app-1")
    store.create("app-2")

    creds = store.list_credentials()
    testbase.assert_equal(len(creds), 2)
    for cred_meta in creds:
        testbase.assert_true("token_hash" not in cred_meta)
        testbase.assert_true("label" in cred_meta)

@testbase.attach.parameter(credstore_db_session, identifier='db_session')
def test_credential_deletion(db_session: Session):
    store = CredentialStore(db_session)
    cred, plain_token = store.create("my-app")

    testbase.assert_true(store.delete(str(cred.id)))
    testbase.assert_true(store.get(str(cred.id)) is None)

if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
