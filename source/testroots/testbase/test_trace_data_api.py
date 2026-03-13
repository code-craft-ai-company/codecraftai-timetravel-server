import pytest
from flask import Flask
from flask_restx import Api
from automojo.timetravelwebsite.restapis.versions.v1.feature.trace_data import publish_namespaces, MOCK_EVENTS, MOCK_CALL_GRAPH, MOCK_VARIABLES

@pytest.fixture
def app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='Test API')
    for ns_obj, ns_path in publish_namespaces("/api/v1"):
        api.add_namespace(ns_obj, ns_path)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}

def test_unauthenticated_request_returns_401(client):
    response = client.get('/api/v1/trace-data/events')
    assert response.status_code == 401

def test_event_query_with_various_filter_combinations(client, auth_headers):
    # Test type filter
    response = client.get('/api/v1/trace-data/events?type=call', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert all(e['type'] == 'call' for e in data['events'])

    # Test function_name filter
    response = client.get('/api/v1/trace-data/events?function_name=process_data', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert all(e['function_name'] == 'process_data' for e in data['events'])

def test_pagination_on_event_queries(client, auth_headers):
    # Get page 1, 2 items
    response = client.get('/api/v1/trace-data/events?page=1&per_page=2', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['events']) == 2
    assert data['events'][0]['id'] == 'evt-1'

    # Get page 2, 2 items
    response = client.get('/api/v1/trace-data/events?page=2&per_page=2', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['events']) == 2
    assert data['events'][0]['id'] == 'evt-3'

def test_timeline_view_returns_correct_structure(client, auth_headers):
    response = client.get('/api/v1/trace-data/timeline?session_id=sess-1', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'timeline' in data

def test_call_graph_view_returns_tree_structure(client, auth_headers):
    response = client.get('/api/v1/trace-data/call-graph?session_id=sess-1', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['function_name'] == "main"
    assert 'children' in data
    assert len(data['children']) == 1

def test_variable_history_returns_chronological_snapshots(client, auth_headers):
    # Variable list
    response = client.get('/api/v1/trace-data/variables?session_id=sess-1', headers=auth_headers)
    assert response.status_code == 200
    assert 'user_count' in response.get_json()['variables']

    # History
    response = client.get('/api/v1/trace-data/variables/user_count/history?session_id=sess-1', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'user_count'
    assert len(data['history']) == 2
    assert data['history'][0]['value'] == '0'
    assert data['history'][1]['value'] == '5'
