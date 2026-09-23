"""
    .. module:: ccai.tests.singlehost.timetravelserver.registration.test_metadata_refresh
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the MetadataRefreshService.
"""

import uuid

from typing import Any, Callable, Dict, List, Optional, Tuple

import ccai.testbase as testbase

from ccai.testshared.factories.timetravelserver.memorydatabase import MemoryDatabase, create_memory_database

from ccai.timetravelserver.persistence.models import RegisteredProcess, PortalSnapshot
from ccai.timetravelserver.registration.metadata_refresh import (
    MetadataRefreshService,
    CommandDispatcher,
    CommandDispatcherError,
)


class ScriptedCommandDispatcher(CommandDispatcher):
    """
        Stand-in for the remote-control command dispatcher.  Every call is recorded and
        answered by the configured ``responder`` callable, which may return a value or
        raise to simulate a remote failure.
    """

    def __init__(self, responder: Optional[Callable[[str, str, Optional[Dict[str, Any]]], Any]] = None):
        self.responder = responder
        self.dispatch_calls: List[Tuple[str, str, Optional[Dict[str, Any]]]] = []
        return

    def dispatch(self, address: str, command: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        self.dispatch_calls.append((address, command, payload))
        if self.responder is None:
            raise ValueError(f"No responder configured for command: {command}")
        result = self.responder(address, command, payload)
        return result


def raise_dispatcher_error(message: str) -> Callable[[str, str, Optional[Dict[str, Any]]], Any]:
    def responder(address: str, command: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        raise CommandDispatcherError(message)
    return responder


def create_test_process(session, state="active"):
    process = RegisteredProcess(
        host="localhost",
        pid=1234,
        application_name="test_app",
        pod_version="1.0.0",
        remote_control_address="localhost:8080",
        lifecycle_state=state
    )
    session.add(process)
    session.commit()
    return process


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_successful_refresh_updates_portal_snapshots(db: MemoryDatabase):
    db_session = db.session
    process = create_test_process(db_session)

    # Mock successful remote calls
    def mock_dispatch(address, command, payload=None):
        if command == "list_portals":
            return [{"name": "web_portal", "is_active": True}, {"name": "admin_portal", "is_active": False}]
        elif command == "get_trace_config":
            return {"level": "info"}
        raise ValueError(f"Unknown command: {command}")

    command_dispatcher = ScriptedCommandDispatcher(responder=mock_dispatch)
    metadata_refresh_service = MetadataRefreshService(db.session_factory, command_dispatcher)

    result = metadata_refresh_service.refresh(process.id)

    assert result.success is True
    assert result.updated_data is not None
    assert len(result.updated_data["portals"]) == 2
    assert result.updated_data["trace_config"] == {"level": "info"}

    # Check snapshots were created
    snapshots = db_session.query(PortalSnapshot).filter_by(process_id=process.id).all()
    assert len(snapshots) == 2

    names = {s.portal_name for s in snapshots}
    assert "web_portal" in names
    assert "admin_portal" in names


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_refresh_with_unreachable_process_returns_failure(db: MemoryDatabase):
    process = create_test_process(db.session)

    command_dispatcher = ScriptedCommandDispatcher(responder=raise_dispatcher_error("Connection refused"))
    metadata_refresh_service = MetadataRefreshService(db.session_factory, command_dispatcher)

    result = metadata_refresh_service.refresh(process.id)

    assert result.success is False
    assert result.error_message == "Connection refused"


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_refresh_does_not_change_lifecycle_state_on_failure(db: MemoryDatabase):
    db_session = db.session
    process = create_test_process(db_session, state="active")

    command_dispatcher = ScriptedCommandDispatcher(responder=raise_dispatcher_error("Connection failed"))
    metadata_refresh_service = MetadataRefreshService(db.session_factory, command_dispatcher)

    metadata_refresh_service.refresh(process.id)

    db_session.refresh(process)
    assert process.lifecycle_state == "active"


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_refresh_with_unknown_process_id_returns_error(db: MemoryDatabase):
    command_dispatcher = ScriptedCommandDispatcher()
    metadata_refresh_service = MetadataRefreshService(db.session_factory, command_dispatcher)

    result = metadata_refresh_service.refresh(uuid.uuid4())

    assert result.success is False
    assert result.error_message == "Process not found"


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_refresh_ignores_disconnected_processes(db: MemoryDatabase):
    process = create_test_process(db.session, state="disconnected")

    command_dispatcher = ScriptedCommandDispatcher()
    metadata_refresh_service = MetadataRefreshService(db.session_factory, command_dispatcher)

    result = metadata_refresh_service.refresh(process.id)

    assert result.success is False
    assert "Cannot refresh disconnected process" in result.error_message


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
