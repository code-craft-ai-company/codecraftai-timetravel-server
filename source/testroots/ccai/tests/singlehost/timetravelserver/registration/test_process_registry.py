"""
    .. module:: ccai.tests.singlehost.timetravelserver.registration.test_process_registry
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the ProcessRegistry.
"""

import time
import uuid

import ccai.testbase as testbase

from ccai.testshared.assertions import assert_raises
from ccai.testshared.factories.timetravelserver.memorydatabase import MemoryDatabase, create_memory_database

from ccai.timetravelserver.persistence.models import RegisteredProcess, PortalSnapshot
from ccai.timetravelserver.registration.process_registry import ProcessRegistry, InvalidProcessStateError


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


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_list_processes_returns_all(db: MemoryDatabase):
    process_registry = ProcessRegistry(db.session_factory)

    create_test_process(db.session, "app1")
    create_test_process(db.session, "app2")

    processes, count = process_registry.list_processes()

    assert count == 2
    assert len(processes) == 2


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_pagination(db: MemoryDatabase):
    process_registry = ProcessRegistry(db.session_factory)

    for i in range(5):
        create_test_process(db.session, f"app{i}")

    processes, count = process_registry.list_processes(offset=2, limit=2)

    assert count == 5
    assert len(processes) == 2


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_state_filtering(db: MemoryDatabase):
    process_registry = ProcessRegistry(db.session_factory)

    create_test_process(db.session, "app1", state="active")
    create_test_process(db.session, "app2", state="stale")
    create_test_process(db.session, "app3", state="active")

    processes, count = process_registry.list_processes(state="active")

    assert count == 2
    assert len(processes) == 2
    assert all(p.lifecycle_state == "active" for p in processes)


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_search_by_app_and_host(db: MemoryDatabase):
    process_registry = ProcessRegistry(db.session_factory)

    create_test_process(db.session, app_name="web_backend", host="server1")
    create_test_process(db.session, app_name="web_frontend", host="server2")
    create_test_process(db.session, app_name="worker", host="server3")

    # Search by app name
    processes, count = process_registry.list_processes(search="web")
    assert count == 2
    assert len(processes) == 2

    # Search by host
    processes, count = process_registry.list_processes(search="server3")
    assert count == 1
    assert len(processes) == 1
    assert processes[0].application_name == "worker"


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_sorting(db: MemoryDatabase):
    process_registry = ProcessRegistry(db.session_factory)

    create_test_process(db.session, "app1")
    create_test_process(db.session, "app2")

    # Wait to ensure different timestamps
    time.sleep(0.1)

    p3 = create_test_process(db.session, "app3")

    processes, _ = process_registry.list_processes(sort_by="registered_at")

    # Default is descending
    assert processes[0].id == p3.id


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_get_process(db: MemoryDatabase):
    process_registry = ProcessRegistry(db.session_factory)

    p = create_test_process(db.session, "app1")

    found = process_registry.get_process(p.id)
    assert found is not None
    assert found.id == p.id


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_get_process_returns_none_for_unknown(db: MemoryDatabase):
    process_registry = ProcessRegistry(db.session_factory)

    assert process_registry.get_process(uuid.uuid4()) is None


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_delete_process_removes_process_and_snapshots(db: MemoryDatabase):
    db_session = db.session
    process_registry = ProcessRegistry(db.session_factory)

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


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_delete_process_rejects_non_disconnected(db: MemoryDatabase):
    process_registry = ProcessRegistry(db.session_factory)

    p = create_test_process(db.session, state="active")

    with assert_raises(InvalidProcessStateError):
        process_registry.delete_process(p.id)


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_get_process_count_by_state(db: MemoryDatabase):
    process_registry = ProcessRegistry(db.session_factory)

    create_test_process(db.session, state="active")
    create_test_process(db.session, state="active")
    create_test_process(db.session, state="stale")
    create_test_process(db.session, state="disconnected")

    counts = process_registry.get_process_count_by_state()

    assert counts.get("active") == 2
    assert counts.get("stale") == 1
    assert counts.get("disconnected") == 1
    assert counts.get("registered", 0) == 0


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
