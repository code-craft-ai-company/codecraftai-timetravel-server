"""
    .. module:: ccai.tests.singlehost.timetravelserver.streamreceiver.test_stream_router
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the StreamRouter.
"""

import threading
from ccai.timetravelserver.streamreceiver.stream_router import StreamRouter

class MockStorageBackend:
    def __init__(self, process_id, session_id):
        self.process_id = process_id
        self.session_id = session_id
        self.committed = False

    def commit(self):
        self.committed = True

class MockSessionUpdater:
    def __init__(self):
        self.updates = {}

    def update_data_reference(self, session_id, uri):
        self.updates[session_id] = uri

def test_routing_creates_separate_storage_for_different_processes():
    def storage_factory(p_id, s_id):
        return MockStorageBackend(p_id, s_id)

    router = StreamRouter(storage_backend_factory=storage_factory)

    storage1 = router.route_stream("proc1", "sess1")
    storage2 = router.route_stream("proc2", "sess1")

    assert storage1.process_id == "proc1"
    assert storage2.process_id == "proc2"
    assert storage1 is not storage2

    assert router.get_data_reference("proc1", "sess1") is storage1
    assert router.get_data_reference("proc2", "sess1") is storage2

def test_routing_creates_separate_storage_for_different_sessions():
    def storage_factory(p_id, s_id):
        return MockStorageBackend(p_id, s_id)

    router = StreamRouter(storage_backend_factory=storage_factory)

    storage1 = router.route_stream("proc1", "sess1")
    storage2 = router.route_stream("proc1", "sess2")

    assert storage1.session_id == "sess1"
    assert storage2.session_id == "sess2"
    assert storage1 is not storage2

def test_concurrent_routing_operations_are_thread_safe():
    def storage_factory(p_id, s_id):
        import time
        time.sleep(0.01) # Simulate some work
        return MockStorageBackend(p_id, s_id)

    router = StreamRouter(storage_backend_factory=storage_factory)

    storages = []

    def worker(p_id, s_id):
        st = router.route_stream(p_id, s_id)
        storages.append(st)

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(f"proc{i}", f"sess{i}"))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(storages) == 10
    assert len(router._routing_table) == 10

    # Check concurrent get
    assert router.get_data_reference("proc5", "sess5") is not None

def test_finalize_route_updates_session_data_reference():
    def storage_factory(p_id, s_id):
        return MockStorageBackend(p_id, s_id)

    updater = MockSessionUpdater()
    router = StreamRouter(storage_backend_factory=storage_factory, session_updater=updater)

    storage = router.route_stream("proc1", "sess1")

    assert router.get_data_reference("proc1", "sess1") is storage

    router.finalize_route("proc1", "sess1", "file:///path/to/data")

    assert storage.committed == True
    assert updater.updates["sess1"] == "file:///path/to/data"
    assert router.get_data_reference("proc1", "sess1") is None # Removed from routing table


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
