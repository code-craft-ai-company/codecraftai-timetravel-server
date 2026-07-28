import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ccai.timetravelserver.persistence.models.base import Base
from ccai.timetravelserver.persistence.models import RegisteredProcess, PortalSnapshot
from ccai.timetravelserver.registration.process_registry import ProcessRegistry
from ccai.timetravelserver.debugcontrol.command_dispatcher import CommandDispatcher, CommandError
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

def test_discover_returns_portal_list(db_session_factory, process_registry, sample_process_id):
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

def test_discover_updates_snapshots(db_session_factory, process_registry, sample_process_id):
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

def test_discover_handles_connection_failure(db_session_factory, process_registry, sample_process_id):
    mock_dispatcher = MockCommandDispatcher(error=ConnectionError("Refused"))
    service = PortalDiscoveryService(db_session_factory, mock_dispatcher, process_registry)

    with pytest.raises(ConnectionError):
        service.discover(sample_process_id)

def test_discover_unknown_process_returns_error(db_session_factory, process_registry):
    mock_dispatcher = MockCommandDispatcher()
    service = PortalDiscoveryService(db_session_factory, mock_dispatcher, process_registry)

    with pytest.raises(ValueError, match="not found"):
        service.discover(uuid.uuid4())
