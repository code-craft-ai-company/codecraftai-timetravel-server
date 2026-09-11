"""
    .. module:: ccai.tests.singlehost.timetravelserver.debugcontrol.test_trace_config
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the TraceConfigService.
"""

import ccai.testbase as testbase

from ccai.testshared.assertions import assert_raises
from ccai.testshared.factories.timetravelserver.memorydatabase import MemoryDatabase, create_memory_database
from ccai.testshared.timetravelserver.processes import add_sample_process

from ccai.timetravelserver.registration.process_registry import ProcessRegistry
from ccai.timetravelserver.debugcontrol.command_dispatcher import CommandDispatcher, CommandError
from ccai.timetravelserver.debugcontrol.trace_config import TraceConfigService, TraceConfigInfo


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


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_get_config_success(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)
    sample_process_id = add_sample_process(db_session_factory)

    mock_dispatcher = MockCommandDispatcher(mock_responses={
        "get_trace_config": {"granularity": "line_level", "record_inner_portals": True}
    })
    service = TraceConfigService(db_session_factory, mock_dispatcher, process_registry)

    config = service.get_config(sample_process_id)
    assert config.granularity == "line_level"
    assert config.record_inner_portals is True

    assert len(mock_dispatcher.dispatch_calls) == 1
    assert mock_dispatcher.dispatch_calls[0][1] == "get_trace_config"


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_update_config_success(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)
    sample_process_id = add_sample_process(db_session_factory)

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


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_update_config_invalid_granularity(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)
    sample_process_id = add_sample_process(db_session_factory)

    mock_dispatcher = MockCommandDispatcher()
    service = TraceConfigService(db_session_factory, mock_dispatcher, process_registry)

    with assert_raises(ValueError, match="Invalid granularity"):
        service.update_config(sample_process_id, granularity="invalid_granularity")


@testbase.attach.parameter(create_memory_database, identifier='db')
def test_connection_failure_returns_descriptive_error(db: MemoryDatabase):
    db_session_factory = db.session_factory
    process_registry = ProcessRegistry(db_session_factory)
    sample_process_id = add_sample_process(db_session_factory)

    mock_dispatcher = MockCommandDispatcher(error=ConnectionError("Refused"))
    service = TraceConfigService(db_session_factory, mock_dispatcher, process_registry)

    with assert_raises(ConnectionError, match="Refused"):
        service.get_config(sample_process_id)


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
