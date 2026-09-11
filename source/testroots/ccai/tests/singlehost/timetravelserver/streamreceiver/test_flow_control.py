"""
    .. module:: ccai.tests.singlehost.timetravelserver.streamreceiver.test_flow_control
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the FlowController back-pressure logic.
"""

import time
from ccai.timetravelserver.streamreceiver.flow_control import FlowController, FlowControlStatus

def test_flow_controller_registration():
    fc = FlowController(high_watermark=1000, low_watermark=500, global_memory_limit=5000)

    fc.register_connection("conn1")
    assert "conn1" in fc.connection_buffers
    assert fc.connection_buffers["conn1"] == 0

    fc.unregister_connection("conn1")
    assert "conn1" not in fc.connection_buffers

def test_buffer_exceeding_high_watermark_returns_pause():
    fc = FlowController(high_watermark=1000, low_watermark=500, global_memory_limit=5000)
    fc.register_connection("conn1")

    # Below high watermark
    assert fc.update_buffer_size("conn1", 800) == FlowControlStatus.OK

    # Exceed high watermark
    assert fc.update_buffer_size("conn1", 1200) == FlowControlStatus.PAUSE

def test_buffer_dropping_below_low_watermark_returns_resume():
    fc = FlowController(high_watermark=1000, low_watermark=500, global_memory_limit=5000)
    fc.register_connection("conn1")

    # Trigger pause
    fc.update_buffer_size("conn1", 1200)

    # Drop below high watermark but above low watermark
    assert fc.update_buffer_size("conn1", 800) == FlowControlStatus.OK

    # Drop below low watermark
    assert fc.update_buffer_size("conn1", 400) == FlowControlStatus.RESUME

def test_global_memory_limit_rejects_new_connections():
    fc = FlowController(high_watermark=1000, low_watermark=500, global_memory_limit=5000)

    fc.register_connection("conn1")
    fc.register_connection("conn2")

    fc.update_buffer_size("conn1", 3000)
    assert fc.should_accept_new() == True

    fc.update_buffer_size("conn2", 2500)
    assert fc.should_accept_new() == False

    fc.unregister_connection("conn1")
    assert fc.should_accept_new() == True

def test_unregister_cleans_up_global_memory():
    fc = FlowController(high_watermark=1000, low_watermark=500, global_memory_limit=5000)

    fc.register_connection("conn1")
    fc.update_buffer_size("conn1", 1000)
    assert fc.global_memory_used == 1000

    fc.unregister_connection("conn1")
    assert fc.global_memory_used == 0

def test_update_buffer_size_unregistered_connection():
    fc = FlowController(high_watermark=1000, low_watermark=500, global_memory_limit=5000)

    assert fc.update_buffer_size("conn1", 1000) == FlowControlStatus.OK


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
