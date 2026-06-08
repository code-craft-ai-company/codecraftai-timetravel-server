"""
    .. module:: ccai.tests.singlehost.timetravelserver.persistence.test_server_config_store
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the ServerConfigStore.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import ccai.testbase as testbase

from ccai.timetravelserver.persistence.models import Base, ServerConfiguration
from ccai.timetravelserver.persistence.server_config_store import ServerConfigStore, CONFIG_SCHEMA

@testbase.register.resource_factory()
def create_db_session() -> Generator[Session, None, None]:
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(bind=engine)
    session = SessionFactory()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()

testbase.originate.parameter(create_db_session, identifier='db_session')

def test_config_get_default(db_session: Session):
    store = ServerConfigStore(db_session)
    val = store.get("listen_port")
    testbase.assert_equal(val, 8080)

def test_config_set_and_get(db_session: Session):
    store = ServerConfigStore(db_session)
    testbase.assert_true(store.set("listen_port", 9090))
    val = store.get("listen_port")
    testbase.assert_equal(val, 9090)

    # test update existing
    testbase.assert_true(store.set("listen_port", 7070))
    val = store.get("listen_port")
    testbase.assert_equal(val, 7070)

def test_config_set_invalid_type(db_session: Session):
    store = ServerConfigStore(db_session)
    testbase.assert_false(store.set("listen_port", "not-an-int"))

def test_config_set_unknown_key(db_session: Session):
    store = ServerConfigStore(db_session)
    testbase.assert_false(store.set("unknown_key", "value"))

def test_config_get_all(db_session: Session):
    db_session.query(ServerConfiguration).delete()
    db_session.commit()

    store = ServerConfigStore(db_session)
    store.set("tls_enabled", True)
    store.set("data_retention_days", 60)

    all_config = store.get_all()
    testbase.assert_equal(all_config["tls_enabled"], True)
    testbase.assert_equal(all_config["data_retention_days"], 60)
    testbase.assert_equal(all_config["listen_port"], 8080) # default

if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
