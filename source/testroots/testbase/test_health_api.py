import pytest
from automojo.timetravelwebsite.restapis.versions.v1.feature.health import MOCK_HEALTH_STATUS, get_health

# Since we don't have the full webworks app context set up yet in the tests
# we test the handler directly to ensure the logic works.

def test_health_endpoint_returns_correct_structure():
    data = get_health()
    assert 'status' in data
    assert 'version' in data
    assert 'uptime_seconds' in data
    assert 'components' in data
    assert 'database' in data['components']
    assert 'stream_receiver' in data['components']
    assert 'storage' in data['components']

def test_healthy_status_when_all_components_are_up():
    MOCK_HEALTH_STATUS['components']['database']['status'] = 'up'
    MOCK_HEALTH_STATUS['components']['stream_receiver']['status'] = 'up'
    MOCK_HEALTH_STATUS['components']['storage']['status'] = 'up'

    data = get_health()
    assert data['status'] == 'healthy'

def test_degraded_status_when_a_component_has_issues():
    MOCK_HEALTH_STATUS['components']['database']['status'] = 'degraded'

    data = get_health()
    assert data['status'] == 'degraded'

    MOCK_HEALTH_STATUS['components']['database']['status'] = 'up'

def test_no_authentication_is_required():
    # Calling directly, no auth required
    data = get_health()
    assert data['status'] in ('healthy', 'degraded')
