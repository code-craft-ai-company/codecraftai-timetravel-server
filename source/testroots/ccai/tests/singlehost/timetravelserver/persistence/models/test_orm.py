"""
    .. module:: ccai.tests.singlehost.timetravelserver.persistence.models.test_orm
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the timetravelserver persistence ORM models.
"""

from typing import Generator

import uuid
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
import ccai.testbase as testbase

from ccai.timetravelserver.persistence.models import (
    Base, User, Credential, RegisteredProcess, PortalSnapshot, TraceSession, ServerConfiguration
)

@testbase.register.resource_factory()
def orm_db_session() -> Generator[Session, None, None]:
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@testbase.attach.parameter(orm_db_session, identifier='db_session')
def test_user_model(db_session: Session):
    user = User(username="testuser", password_hash="hash123", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    queried_user = db_session.query(User).filter_by(username="testuser").first()
    testbase.assert_equal(queried_user.username, "testuser")
    testbase.assert_equal(queried_user.role, "viewer")
    testbase.assert_true(isinstance(queried_user.id, uuid.UUID))

@testbase.attach.parameter(orm_db_session, identifier='db_session')
def test_user_unique_constraint(db_session: Session):
    user1 = User(username="testuser2", password_hash="hash1")
    db_session.add(user1)
    db_session.commit()

    user2 = User(username="testuser2", password_hash="hash2")
    db_session.add(user2)

    try:
        db_session.commit()
        testbase.assert_true(False, "Should have raised IntegrityError for duplicate username")
    except IntegrityError:
        db_session.rollback()

@testbase.attach.parameter(orm_db_session, identifier='db_session')
def test_credential_model(db_session: Session):
    cred = Credential(token_hash="hash_abc", label="my-token")
    db_session.add(cred)
    db_session.commit()

    queried_cred = db_session.query(Credential).filter_by(label="my-token").first()
    testbase.assert_equal(queried_cred.token_hash, "hash_abc")
    testbase.assert_true(queried_cred.expires_at is None)

@testbase.attach.parameter(orm_db_session, identifier='db_session')
def test_process_model(db_session: Session):
    process = RegisteredProcess(host="localhost", pid=1234, application_name="test_app")
    db_session.add(process)
    db_session.commit()

    queried_process = db_session.query(RegisteredProcess).filter_by(pid=1234).first()
    testbase.assert_equal(queried_process.lifecycle_state, "registered")
    testbase.assert_equal(queried_process.host, "localhost")

@testbase.attach.parameter(orm_db_session, identifier='db_session')
def test_portal_snapshot_model(db_session: Session):
    process = RegisteredProcess(host="localhost", pid=5678)
    db_session.add(process)
    db_session.commit()

    snapshot = PortalSnapshot(process_id=process.id, portal_name="test_portal", is_active=True)
    db_session.add(snapshot)
    db_session.commit()

    queried_snapshot = db_session.query(PortalSnapshot).filter_by(portal_name="test_portal").first()
    testbase.assert_equal(queried_snapshot.is_active, True)
    testbase.assert_equal(queried_snapshot.process_id, process.id)

@testbase.attach.parameter(orm_db_session, identifier='db_session')
def test_trace_session_model(db_session: Session):
    process = RegisteredProcess(host="localhost", pid=9999)
    db_session.add(process)
    db_session.commit()

    tsession = TraceSession(process_id=process.id, data_reference="/tmp/trace1")
    db_session.add(tsession)
    db_session.commit()

    queried_session = db_session.query(TraceSession).filter_by(data_reference="/tmp/trace1").first()
    testbase.assert_equal(queried_session.status, "active")
    testbase.assert_equal(queried_session.process_id, process.id)

@testbase.attach.parameter(orm_db_session, identifier='db_session')
def test_server_config_model(db_session: Session):
    config = ServerConfiguration(key="max_connections", value="100")
    db_session.add(config)
    db_session.commit()

    queried_config = db_session.query(ServerConfiguration).filter_by(key="max_connections").first()
    testbase.assert_equal(queried_config.value, "100")

@testbase.attach.parameter(orm_db_session, identifier='db_session')
def test_server_config_unique_constraint(db_session: Session):
    config1 = ServerConfiguration(key="timeout", value="30")
    db_session.add(config1)
    db_session.commit()

    config2 = ServerConfiguration(key="timeout", value="60")
    db_session.add(config2)

    try:
        db_session.commit()
        testbase.assert_true(False, "Should have raised IntegrityError for duplicate config key")
    except IntegrityError:
        db_session.rollback()

def test_alembic_upgrade_downgrade():
    """
        The migration chain applies and reverses cleanly.

        Three things this test used to get wrong, all of which made it fail
        or contaminate the run rather than test the migrations:

        - it invoked bare `alembic`, which requires the venv's bin on PATH
          and raised FileNotFoundError under the test runner. Going through
          `sys.executable -m alembic` needs no PATH entry at all;
        - it assigned `os.environ["PYTHONPATH"] = "/app/source/packages/"`,
          a hardcoded container path, into the CURRENT process — so it both
          pointed at nothing on a developer machine and leaked into every
          test that ran afterwards. The child now gets its own env copy;
        - its `cwd` was relative, so it only worked when the runner happened
          to start at the repository root. It is derived from this file's
          location now.
    """
    import os
    import subprocess
    import sys

    # Walk up to the repository root rather than counting `..` levels — this
    # file is eight directories deep and a hand-counted offset is exactly the
    # kind of thing that silently resolves to the wrong place (it did: the
    # cwd did not exist, which surfaces as FileNotFoundError from subprocess
    # and looks identical to a missing executable).
    repo_root = os.path.dirname(os.path.abspath(__file__))
    while repo_root != os.path.dirname(repo_root):
        if os.path.isfile(os.path.join(repo_root, "pyproject.toml")):
            break
        repo_root = os.path.dirname(repo_root)
    packages_dir = os.path.join(repo_root, "source", "packages")
    migrations_dir = os.path.join(packages_dir, "ccai", "timetravelserver", "persistence")

    child_env = dict(os.environ)
    existing = child_env.get("PYTHONPATH", "")
    child_env["PYTHONPATH"] = (f"{packages_dir}{os.pathsep}{existing}"
                               if existing else packages_dir)

    try:
        for args in (["downgrade", "base"], ["upgrade", "head"]):
            subprocess.run([sys.executable, "-m", "alembic", *args],
                           cwd=migrations_dir, env=child_env,
                           check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        testbase.assert_true(False, f"Alembic migration failed: {e.stderr.decode('utf-8')}")

if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
