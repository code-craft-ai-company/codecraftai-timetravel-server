import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from automojo.timetravelserver.persistence.models.base import Base
from automojo.timetravelserver.persistence.models import RegisteredProcess
from automojo.timetravelserver.registration.process_registry import ProcessRegistry
from automojo.timetravelserver.debugcontrol.command_dispatcher import CommandDispatcher, CommandError
from automojo.timetravelserver.debugcontrol.trace_config import TraceConfigService, TraceConfigInfo

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

        return self.mock_responses.get(command, {})

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

def test_get_config_success(db_session_factory, process_registry, sample_process_id):
    mock_dispatcher = MockCommandDispatcher(mock_responses={
        "get_trace_config": {"granularity": "line_level", "record_inner_portals": True}
    })
    service = TraceConfigService(db_session_factory, mock_dispatcher, process_registry)

    config = service.get_config(sample_process_id)
    assert config.granularity == "line_level"
    assert config.record_inner_portals is True

    assert len(mock_dispatcher.dispatch_calls) == 1
    assert mock_dispatcher.dispatch_calls[0][1] == "get_trace_config"

def test_update_config_success(db_session_factory, process_registry, sample_process_id):
    mock_dispatcher = MockCommandDispatcher(mock_responses={
        "update_trace_config": {"granularity": "variable_snapshot", "record_inner_portals": False}
    })
    service = TraceConfigService(db_session_factory, mock_dispatcher, process_registry)

    config = service.update_config(sample_process_id, granularity="variable_snapshot", record_inner_portals=False)
    assert config.granularity == "variable_snapshot"
    assert config.record_inner_portals is False

    assert len(mock_dispatcher.dispatch_calls) == 1
    assert mock_dispatcher.dispatch_calls[0][1] == "update_trace_config"
    assert mock_dispatcher.dispatch_calls[0][2] == {
        "granularity": "variable_snapshot",
        "record_inner_portals": False
    }

def test_update_config_invalid_granularity(db_session_factory, process_registry, sample_process_id):
    mock_dispatcher = MockCommandDispatcher()
    service = TraceConfigService(db_session_factory, mock_dispatcher, process_registry)

    with pytest.raises(ValueError, match="Invalid granularity"):
        service.update_config(sample_process_id, granularity="invalid_granularity")

def test_connection_failure_returns_descriptive_error(db_session_factory, process_registry, sample_process_id):
    mock_dispatcher = MockCommandDispatcher(error=ConnectionError("Refused"))
    service = TraceConfigService(db_session_factory, mock_dispatcher, process_registry)

    with pytest.raises(ConnectionError, match="Refused"):
        service.get_config(sample_process_id)
