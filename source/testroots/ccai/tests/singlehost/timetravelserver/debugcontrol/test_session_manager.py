"""
    .. module:: ccai.tests.singlehost.timetravelserver.debugcontrol.test_session_manager
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the DebugSessionManager.
"""

import uuid

import ccai.testbase as testbase

from ccai.testshared.assertions import assert_raises
from ccai.testshared.factories.timetravelserver.memorydatabase import MemoryDatabase, create_memory_database
from ccai.testshared.timetravelserver.processes import add_sample_process

from ccai.timetravelserver.registration.process_registry import ProcessRegistry
from ccai.timetravelserver.debugcontrol.session_manager import DebugSessionManager


def create_session_manager(db: MemoryDatabase) -> DebugSessionManager:
    process_registry = ProcessRegistry(db.session_factory)
    session_manager = DebugSessionManager(db.session_factory, process_registry)
    return session_manager


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_create_session(db: MemoryDatabase):
    session_manager = create_session_manager(db)
    sample_process_id = add_sample_process(db.session_factory, remote_control_address=None)

    trace_session = session_manager.create_session(sample_process_id, ["portal1"])
    assert trace_session.id is not None
    assert trace_session.process_id == sample_process_id
    assert trace_session.status == "active"
    assert trace_session.started_at is not None
    assert trace_session.stopped_at is None


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_create_session_invalid_process(db: MemoryDatabase):
    session_manager = create_session_manager(db)

    with assert_raises(ValueError, match="not found"):
        session_manager.create_session(uuid.uuid4(), ["portal1"])


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_close_session(db: MemoryDatabase):
    session_manager = create_session_manager(db)
    sample_process_id = add_sample_process(db.session_factory, remote_control_address=None)

    trace_session = session_manager.create_session(sample_process_id, ["portal1"])
    assert trace_session.status == "active"

    closed_session = session_manager.close_session(trace_session.id)
    assert closed_session.status == "completed"
    assert closed_session.stopped_at is not None
    assert closed_session.id == trace_session.id


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_list_sessions_by_process_id(db: MemoryDatabase):
    session_manager = create_session_manager(db)
    sample_process_id = add_sample_process(db.session_factory, remote_control_address=None)

    # Create a second process
    proc2_id = add_sample_process(db.session_factory, application_name="test-app-2", pid=5678,
                                  remote_control_address=None)

    session_manager.create_session(sample_process_id, ["portal1"])
    session_manager.create_session(sample_process_id, ["portal2"])
    session_manager.create_session(proc2_id, ["portal3"])

    sessions = session_manager.list_sessions(process_id=sample_process_id)
    assert len(sessions) == 2
    for s in sessions:
        assert s.process_id == sample_process_id


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_list_sessions_by_status(db: MemoryDatabase):
    session_manager = create_session_manager(db)
    sample_process_id = add_sample_process(db.session_factory, remote_control_address=None)

    s1 = session_manager.create_session(sample_process_id, ["portal1"])
    s2 = session_manager.create_session(sample_process_id, ["portal2"])
    session_manager.close_session(s1.id)

    active_sessions = session_manager.list_sessions(status="active")
    assert len(active_sessions) == 1
    assert active_sessions[0].id == s2.id

    completed_sessions = session_manager.list_sessions(status="completed")
    assert len(completed_sessions) == 1
    assert completed_sessions[0].id == s1.id


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_get_session(db: MemoryDatabase):
    session_manager = create_session_manager(db)
    sample_process_id = add_sample_process(db.session_factory, remote_control_address=None)

    created = session_manager.create_session(sample_process_id, ["portal1"])
    retrieved = session_manager.get_session(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id

    assert session_manager.get_session(uuid.uuid4()) is None


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_update_data_reference(db: MemoryDatabase):
    session_manager = create_session_manager(db)
    sample_process_id = add_sample_process(db.session_factory, remote_control_address=None)

    trace_session = session_manager.create_session(sample_process_id, ["portal1"])
    assert trace_session.data_reference is None

    session_manager.update_data_reference(trace_session.id, "storage/path/to/data")

    updated = session_manager.get_session(trace_session.id)
    assert updated.data_reference == "storage/path/to/data"


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
