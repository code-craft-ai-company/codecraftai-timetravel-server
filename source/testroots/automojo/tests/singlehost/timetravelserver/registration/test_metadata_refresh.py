import pytest
import uuid
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import MagicMock

from automojo.timetravelserver.persistence.models.base import Base
from automojo.timetravelserver.persistence.models import RegisteredProcess, PortalSnapshot
from automojo.timetravelserver.registration.metadata_refresh import (
    MetadataRefreshService, CommandDispatcher, RefreshResult, CommandDispatcherError
)

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
def command_dispatcher():
    return MagicMock(spec=CommandDispatcher)

@pytest.fixture
def metadata_refresh_service(db_session_factory, command_dispatcher):
    return MetadataRefreshService(db_session_factory, command_dispatcher)

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

def test_successful_refresh_updates_portal_snapshots(db_session, command_dispatcher, metadata_refresh_service):
    process = create_test_process(db_session)

    # Mock successful remote calls
    def mock_dispatch(address, command, payload=None):
        if command == "list_portals":
            return [{"name": "web_portal", "is_active": True}, {"name": "admin_portal", "is_active": False}]
        elif command == "get_trace_config":
            return {"level": "info"}
        raise ValueError(f"Unknown command: {command}")

    command_dispatcher.dispatch.side_effect = mock_dispatch

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

def test_refresh_with_unreachable_process_returns_failure(db_session, command_dispatcher, metadata_refresh_service):
    process = create_test_process(db_session)

    command_dispatcher.dispatch.side_effect = CommandDispatcherError("Connection refused")

    result = metadata_refresh_service.refresh(process.id)

    assert result.success is False
    assert result.error_message == "Connection refused"

def test_refresh_does_not_change_lifecycle_state_on_failure(db_session, command_dispatcher, metadata_refresh_service):
    process = create_test_process(db_session, state="active")

    command_dispatcher.dispatch.side_effect = CommandDispatcherError("Connection failed")

    metadata_refresh_service.refresh(process.id)

    db_session.refresh(process)
    assert process.lifecycle_state == "active"

def test_refresh_with_unknown_process_id_returns_error(metadata_refresh_service):
    result = metadata_refresh_service.refresh(uuid.uuid4())

    assert result.success is False
    assert result.error_message == "Process not found"

def test_refresh_ignores_disconnected_processes(db_session, metadata_refresh_service):
    process = create_test_process(db_session, state="disconnected")

    result = metadata_refresh_service.refresh(process.id)

    assert result.success is False
    assert "Cannot refresh disconnected process" in result.error_message
