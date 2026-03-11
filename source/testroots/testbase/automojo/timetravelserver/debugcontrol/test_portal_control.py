import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from automojo.timetravelserver.persistence.models.base import Base
from automojo.timetravelserver.persistence.models import RegisteredProcess, PortalSnapshot
from automojo.timetravelserver.registration.process_registry import ProcessRegistry
from automojo.timetravelserver.debugcontrol.command_dispatcher import CommandDispatcher, CommandError
from automojo.timetravelserver.debugcontrol.portal_control import PortalControlService

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

@pytest.fixture
def db_session_factory():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

@pytest.fixture
def process_registry(db_session_factory):
    return ProcessRegistry(db_session_factory)

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
            lifecycle_state="connected",
            remote_control_address="127.0.0.1:9000"
        )
        session.add(proc)
        session.commit()
        return proc.id
    finally:
        session.close()

def test_activate_portal_success(db_session_factory, process_registry, sample_process_id):
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

def test_deactivate_portal_success(db_session_factory, process_registry, sample_process_id):
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

def test_activate_portals_bulk(db_session_factory, process_registry, sample_process_id):
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

def test_error_propagation_from_remote(db_session_factory, process_registry, sample_process_id):
    mock_dispatcher = MockCommandDispatcher(error=CommandError("Remote fail"))
    service = PortalControlService(db_session_factory, mock_dispatcher, process_registry)

    with pytest.raises(CommandError):
        service.activate_portal(sample_process_id, "portal1")

def test_unreachable_process_returns_error(db_session_factory, process_registry):
    mock_dispatcher = MockCommandDispatcher()
    service = PortalControlService(db_session_factory, mock_dispatcher, process_registry)

    with pytest.raises(ValueError, match="not found"):
        service.activate_portal(uuid.uuid4(), "portal1")
