"""
    .. module:: ccai.tests.singlehost.timetravelserver.debugcontrol.test_portal_discovery
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the PortalDiscoveryService.
"""

import uuid

import ccai.testbase as testbase

from ccai.testshared.assertions import assert_raises
from ccai.testshared.factories.timetravelserver.memorydatabase import MemoryDatabase, create_memory_database
from ccai.testshared.timetravelserver.processes import add_sample_process

from ccai.timetravelserver.persistence.models import PortalSnapshot
from ccai.timetravelserver.registration.process_registry import ProcessRegistry
from ccai.timetravelserver.debugcontrol.command_dispatcher import CommandDispatcher
from ccai.timetravelserver.debugcontrol.portal_discovery import PortalDiscoveryService, PortalInfo


class MockCommandDispatcher(CommandDispatcher):
    def __init__(self, mock_response_data=None, error=None):
        super().__init__("token")
        self.mock_response_data = mock_response_data or {}
        self.error = error
        self.dispatch_calls = []

    def dispatch(self, remote_address: str, command: str, params=None):
        self.dispatch_calls.append((remote_address, command, params))
        if self.error:
            raise self.error
        return self.mock_response_data


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_discover_returns_portal_list(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)
    sample_process_id = add_sample_process(db_session_factory)

    mock_dispatcher = MockCommandDispatcher(mock_response_data={
        "portals": [
            {"name": "portal1", "is_active": True},
            {"name": "portal2", "is_active": False}
        ]
    })
    service = PortalDiscoveryService(db_session_factory, mock_dispatcher, process_registry)

    portals = service.discover(sample_process_id)
    assert len(portals) == 2
    assert portals[0] == PortalInfo(name="portal1", is_active=True)
    assert portals[1] == PortalInfo(name="portal2", is_active=False)

    assert len(mock_dispatcher.dispatch_calls) == 1
    assert mock_dispatcher.dispatch_calls[0][0] == "127.0.0.1:9000"
    assert mock_dispatcher.dispatch_calls[0][1] == "list_portals"


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_discover_updates_snapshots(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)
    sample_process_id = add_sample_process(db_session_factory)

    # Pre-populate snapshot to test update and deletion
    session = db_session_factory()
    try:
        session.add(PortalSnapshot(process_id=sample_process_id, portal_name="old_portal", is_active=True))
        session.add(PortalSnapshot(process_id=sample_process_id, portal_name="portal_to_update", is_active=False))
        session.commit()
    finally:
        session.close()

    mock_dispatcher = MockCommandDispatcher(mock_response_data={
        "portals": [
            {"name": "portal_to_update", "is_active": True},
            {"name": "new_portal", "is_active": True}
        ]
    })
    service = PortalDiscoveryService(db_session_factory, mock_dispatcher, process_registry)

    service.discover(sample_process_id)

    # Check DB
    session = db_session_factory()
    try:
        snapshots = session.query(PortalSnapshot).filter_by(process_id=sample_process_id).all()
        assert len(snapshots) == 2

        snapshot_map = {s.portal_name: s.is_active for s in snapshots}
        assert "old_portal" not in snapshot_map
        assert snapshot_map["portal_to_update"] is True
        assert snapshot_map["new_portal"] is True
    finally:
        session.close()


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_discover_handles_connection_failure(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)
    sample_process_id = add_sample_process(db_session_factory)

    mock_dispatcher = MockCommandDispatcher(error=ConnectionError("Refused"))
    service = PortalDiscoveryService(db_session_factory, mock_dispatcher, process_registry)

    with assert_raises(ConnectionError):
        service.discover(sample_process_id)


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_discover_unknown_process_returns_error(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)

    mock_dispatcher = MockCommandDispatcher()
    service = PortalDiscoveryService(db_session_factory, mock_dispatcher, process_registry)

    with assert_raises(ValueError, match="not found"):
        service.discover(uuid.uuid4())


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
