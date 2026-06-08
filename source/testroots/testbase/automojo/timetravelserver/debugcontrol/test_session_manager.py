import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ccai.timetravelserver.persistence.models.base import Base
from ccai.timetravelserver.persistence.models import RegisteredProcess, TraceSession
from ccai.timetravelserver.registration.process_registry import ProcessRegistry
from ccai.timetravelserver.debugcontrol.session_manager import DebugSessionManager

@pytest.fixture
def db_session_factory():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

@pytest.fixture
def process_registry(db_session_factory):
    return ProcessRegistry(db_session_factory)

@pytest.fixture
def session_manager(db_session_factory, process_registry):
    return DebugSessionManager(db_session_factory, process_registry)

@pytest.fixture
def sample_process_id(db_session_factory):
    session = db_session_factory()
    try:
        proc = RegisteredProcess(
            id=uuid.uuid4(),
            application_name="test-app",
            host="localhost",
            pid=1234,
            pod_version="1.0",
            lifecycle_state="connected"
        )
        session.add(proc)
        session.commit()
        return proc.id
    finally:
        session.close()

def test_create_session(session_manager, sample_process_id):
    trace_session = session_manager.create_session(sample_process_id, ["portal1"])
    assert trace_session.id is not None
    assert trace_session.process_id == sample_process_id
    assert trace_session.status == "active"
    assert trace_session.started_at is not None
    assert trace_session.stopped_at is None

def test_create_session_invalid_process(session_manager):
    with pytest.raises(ValueError, match="not found"):
        session_manager.create_session(uuid.uuid4(), ["portal1"])

def test_close_session(session_manager, sample_process_id):
    trace_session = session_manager.create_session(sample_process_id, ["portal1"])
    assert trace_session.status == "active"

    closed_session = session_manager.close_session(trace_session.id)
    assert closed_session.status == "completed"
    assert closed_session.stopped_at is not None
    assert closed_session.id == trace_session.id

def test_list_sessions_by_process_id(session_manager, sample_process_id, db_session_factory):
    # Create a second process
    session = db_session_factory()
    try:
        proc2 = RegisteredProcess(
            id=uuid.uuid4(),
            application_name="test-app-2",
            host="localhost",
            pid=5678,
            pod_version="1.0",
            lifecycle_state="connected"
        )
        session.add(proc2)
        session.commit()
        proc2_id = proc2.id
    finally:
        session.close()

    session_manager.create_session(sample_process_id, ["portal1"])
    session_manager.create_session(sample_process_id, ["portal2"])
    session_manager.create_session(proc2_id, ["portal3"])

    sessions = session_manager.list_sessions(process_id=sample_process_id)
    assert len(sessions) == 2
    for s in sessions:
        assert s.process_id == sample_process_id

def test_list_sessions_by_status(session_manager, sample_process_id):
    s1 = session_manager.create_session(sample_process_id, ["portal1"])
    s2 = session_manager.create_session(sample_process_id, ["portal2"])
    session_manager.close_session(s1.id)

    active_sessions = session_manager.list_sessions(status="active")
    assert len(active_sessions) == 1
    assert active_sessions[0].id == s2.id

    completed_sessions = session_manager.list_sessions(status="completed")
    assert len(completed_sessions) == 1
    assert completed_sessions[0].id == s1.id

def test_get_session(session_manager, sample_process_id):
    created = session_manager.create_session(sample_process_id, ["portal1"])
    retrieved = session_manager.get_session(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id

    assert session_manager.get_session(uuid.uuid4()) is None

def test_update_data_reference(session_manager, sample_process_id):
    trace_session = session_manager.create_session(sample_process_id, ["portal1"])
    assert trace_session.data_reference is None

    session_manager.update_data_reference(trace_session.id, "storage/path/to/data")

    updated = session_manager.get_session(trace_session.id)
    assert updated.data_reference == "storage/path/to/data"
