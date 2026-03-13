import pytest
from automojo.timetravelwebsite.restapis.versions.v1.feature.trace_data import (
    MOCK_EVENTS, MOCK_CALL_GRAPH, MOCK_VARIABLES, RequireAuth,
    list_trace_events, get_trace_timeline, get_trace_call_graph,
    get_trace_variables, get_trace_variable_history
)

class MockRequest:
    def __init__(self, headers):
        self.headers = headers

def test_unauthenticated_request_returns_401():
    policy = RequireAuth()
    assert not policy.check_access(MockRequest({}))

def test_event_query_with_various_filter_combinations():
    # Test type filter
    data = list_trace_events(type='call')
    assert all(e['type'] == 'call' for e in data['events'])

    # Test function_name filter
    data = list_trace_events(function_name='process_data')
    assert all(e['function_name'] == 'process_data' for e in data['events'])

def test_pagination_on_event_queries():
    # Get page 1, 2 items
    data = list_trace_events(page=1, per_page=2)
    assert len(data['events']) == 2
    assert data['events'][0]['id'] == 'evt-1'

    # Get page 2, 2 items
    data = list_trace_events(page=2, per_page=2)
    assert len(data['events']) == 2
    assert data['events'][0]['id'] == 'evt-3'

def test_timeline_view_returns_correct_structure():
    data = get_trace_timeline(session_id="sess-1")
    assert 'timeline' in data

def test_call_graph_view_returns_tree_structure():
    data = get_trace_call_graph(session_id="sess-1")
    assert data['function_name'] == "main"
    assert 'children' in data
    assert len(data['children']) == 1

def test_variable_history_returns_chronological_snapshots():
    # Variable list
    data = get_trace_variables(session_id="sess-1")
    assert 'user_count' in data['variables']

    # History
    data = get_trace_variable_history(name="user_count", session_id="sess-1")
    assert data['name'] == 'user_count'
    assert len(data['history']) == 2
    assert data['history'][0]['value'] == '0'
    assert data['history'][1]['value'] == '5'
