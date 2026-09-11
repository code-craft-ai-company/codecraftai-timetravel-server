"""
    .. module:: ccai.tests.singlehost.timetravelserver.debugcontrol.test_portal_control
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the PortalControlService.
"""

import uuid

import ccai.testbase as testbase

from ccai.testshared.assertions import assert_raises
from ccai.testshared.factories.timetravelserver.memorydatabase import MemoryDatabase, create_memory_database
from ccai.testshared.timetravelserver.processes import add_sample_process

from ccai.timetravelserver.persistence.models import PortalSnapshot
from ccai.timetravelserver.registration.process_registry import ProcessRegistry
from ccai.timetravelserver.debugcontrol.command_dispatcher import CommandDispatcher, CommandError
from ccai.timetravelserver.debugcontrol.portal_control import PortalControlService


class MockCommandDispatcher(CommandDispatcher):
    def __init__(self, mock_responses=None, error=None):
        super().__init__("token")
        self.mock_responses = mock_responses or {}
        self.error = error
        self.dispatch_calls = []

    def dispatch(self, remote_address: str, command: str, params=None):
        self.dispatch_calls.append((remote_address, command, params))
        if self.error:
            raise self.error

        key = (command, params.get("portal_name")) if params else command
        return self.mock_responses.get(key, {"success": True})


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_activate_portal_success(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)
    sample_process_id = add_sample_process(db_session_factory)

    mock_dispatcher = MockCommandDispatcher()
    service = PortalControlService(db_session_factory, mock_dispatcher, process_registry)

    success = service.activate_portal(sample_process_id, "portal1")
    assert success is True

    assert len(mock_dispatcher.dispatch_calls) == 1
    assert mock_dispatcher.dispatch_calls[0][1] == "activate_portal"
    assert mock_dispatcher.dispatch_calls[0][2] == {"portal_name": "portal1"}

    session = db_session_factory()
    snapshot = session.query(PortalSnapshot).filter_by(process_id=sample_process_id, portal_name="portal1").one()
    assert snapshot.is_active is True
    session.close()


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_deactivate_portal_success(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)
    sample_process_id = add_sample_process(db_session_factory)

    mock_dispatcher = MockCommandDispatcher()
    service = PortalControlService(db_session_factory, mock_dispatcher, process_registry)

    success = service.deactivate_portal(sample_process_id, "portal1")
    assert success is True

    assert len(mock_dispatcher.dispatch_calls) == 1
    assert mock_dispatcher.dispatch_calls[0][1] == "deactivate_portal"
    assert mock_dispatcher.dispatch_calls[0][2] == {"portal_name": "portal1"}

    session = db_session_factory()
    snapshot = session.query(PortalSnapshot).filter_by(process_id=sample_process_id, portal_name="portal1").one()
    assert snapshot.is_active is False
    session.close()


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_activate_portals_bulk(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)
    sample_process_id = add_sample_process(db_session_factory)

    responses = {
        ("activate_portal", "portal1"): {"success": True},
        ("activate_portal", "portal2"): {"success": False}
    }
    mock_dispatcher = MockCommandDispatcher(mock_responses=responses)
    service = PortalControlService(db_session_factory, mock_dispatcher, process_registry)

    results = service.activate_portals(sample_process_id, ["portal1", "portal2"])
    assert results == {"portal1": True, "portal2": False}

    session = db_session_factory()
    s1 = session.query(PortalSnapshot).filter_by(portal_name="portal1").one()
    assert s1.is_active is True

    s2 = session.query(PortalSnapshot).filter_by(portal_name="portal2").one_or_none()
    assert s2 is None  # since success was false, snapshot wasn't updated
    session.close()


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_error_propagation_from_remote(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)
    sample_process_id = add_sample_process(db_session_factory)

    mock_dispatcher = MockCommandDispatcher(error=CommandError("Remote fail"))
    service = PortalControlService(db_session_factory, mock_dispatcher, process_registry)

    with assert_raises(CommandError):
        service.activate_portal(sample_process_id, "portal1")


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_unreachable_process_returns_error(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)

    mock_dispatcher = MockCommandDispatcher()
    service = PortalControlService(db_session_factory, mock_dispatcher, process_registry)

    with assert_raises(ValueError, match="not found"):
        service.activate_portal(uuid.uuid4(), "portal1")


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
