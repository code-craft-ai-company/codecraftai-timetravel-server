import pytest
import uuid
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ccai.timetravelserver.persistence.models.base import Base
from ccai.timetravelserver.persistence.models import RegisteredProcess, PortalSnapshot
from ccai.timetravelserver.registration.process_registry import ProcessRegistry, InvalidProcessStateError

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
def process_registry(db_session_factory):
    return ProcessRegistry(db_session_factory)

def create_test_process(session, app_name="test_app", host="localhost", state="registered"):
    process = RegisteredProcess(
        host=host,
        pid=1234,
        application_name=app_name,
        pod_version="1.0.0",
        remote_control_address=f"{host}:8080",
        lifecycle_state=state
    )
    session.add(process)
    session.commit()
    return process

def test_list_processes_returns_all(db_session, process_registry):
    create_test_process(db_session, "app1")
    create_test_process(db_session, "app2")

    processes, count = process_registry.list_processes()

    assert count == 2
    assert len(processes) == 2

def test_pagination(db_session, process_registry):
    for i in range(5):
        create_test_process(db_session, f"app{i}")

    processes, count = process_registry.list_processes(offset=2, limit=2)

    assert count == 5
    assert len(processes) == 2

def test_state_filtering(db_session, process_registry):
    create_test_process(db_session, "app1", state="active")
    create_test_process(db_session, "app2", state="stale")
    create_test_process(db_session, "app3", state="active")

    processes, count = process_registry.list_processes(state="active")

    assert count == 2
    assert len(processes) == 2
    assert all(p.lifecycle_state == "active" for p in processes)

def test_search_by_app_and_host(db_session, process_registry):
    create_test_process(db_session, app_name="web_backend", host="server1")
    create_test_process(db_session, app_name="web_frontend", host="server2")
    create_test_process(db_session, app_name="worker", host="server3")

    # Search by app name
    processes, count = process_registry.list_processes(search="web")
    assert count == 2
    assert len(processes) == 2

    # Search by host
    processes, count = process_registry.list_processes(search="server3")
    assert count == 1
    assert len(processes) == 1
    assert processes[0].application_name == "worker"

def test_sorting(db_session, process_registry):
    p1 = create_test_process(db_session, "app1")
    p2 = create_test_process(db_session, "app2")

    # Wait to ensure different timestamps
    import time
    time.sleep(0.1)

    p3 = create_test_process(db_session, "app3")

    processes, _ = process_registry.list_processes(sort_by="registered_at")

    # Default is descending
    assert processes[0].id == p3.id

def test_get_process(db_session, process_registry):
    p = create_test_process(db_session, "app1")

    found = process_registry.get_process(p.id)
    assert found is not None
    assert found.id == p.id

def test_get_process_returns_none_for_unknown(process_registry):
    assert process_registry.get_process(uuid.uuid4()) is None

def test_delete_process_removes_process_and_snapshots(db_session, process_registry):
    p = create_test_process(db_session, state="disconnected")

    snapshot = PortalSnapshot(
        process_id=p.id,
        portal_name="test_portal",
        is_active=False
    )
    db_session.add(snapshot)
    db_session.commit()

    process_registry.delete_process(p.id)

    assert process_registry.get_process(p.id) is None

    # Check snapshot is deleted
    snapshots = db_session.query(PortalSnapshot).filter_by(process_id=p.id).all()
    assert len(snapshots) == 0

def test_delete_process_rejects_non_disconnected(db_session, process_registry):
    p = create_test_process(db_session, state="active")

    with pytest.raises(InvalidProcessStateError):
        process_registry.delete_process(p.id)

def test_get_process_count_by_state(db_session, process_registry):
    create_test_process(db_session, state="active")
    create_test_process(db_session, state="active")
    create_test_process(db_session, state="stale")
    create_test_process(db_session, state="disconnected")

    counts = process_registry.get_process_count_by_state()

    assert counts.get("active") == 2
    assert counts.get("stale") == 1
    assert counts.get("disconnected") == 1
    assert counts.get("registered", 0) == 0
