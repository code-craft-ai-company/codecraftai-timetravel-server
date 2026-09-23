"""
    .. module:: ccai.tests.singlehost.timetravelserver.persistence.trace_storage.test_filesystem_backend
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for the FilesystemTraceStorage backend.
"""

import os
import shutil
import tempfile
import datetime
from pathlib import Path
from typing import Generator
import ccai.testbase as testbase

from ccai.timetravelserver.persistence.trace_storage import FilesystemTraceStorage

@testbase.register.resource_factory()
def fsbackend_trace_storage() -> Generator[FilesystemTraceStorage, None, None]:
    temp_dir = tempfile.mkdtemp()
    storage = FilesystemTraceStorage(temp_dir)
    yield storage
    shutil.rmtree(temp_dir)


@testbase.attach.parameter(fsbackend_trace_storage, identifier='storage')
def test_write_read_roundtrip(storage: FilesystemTraceStorage):
    data = b"hello trace data"
    session_id = "session_123"
    ref = storage.write(data, session_id)
    final_ref = storage.finalize(ref)

    read_data = storage.read(final_ref)
    testbase.assert_equal(read_data, data)

@testbase.attach.parameter(fsbackend_trace_storage, identifier='storage')
def test_append_accumulates_data(storage: FilesystemTraceStorage):
    session_id = "session_456"
    ref = storage.write(b"part1", session_id)
    storage.append(ref, b"part2")
    final_ref = storage.finalize(ref)

    read_data = storage.read(final_ref)
    testbase.assert_equal(read_data, b"part1part2")

@testbase.attach.parameter(fsbackend_trace_storage, identifier='storage')
def test_read_non_existent(storage: FilesystemTraceStorage):
    try:
        storage.read("/tmp/does_not_exist.trace")
        testbase.assert_true(False, "Should have raised FileNotFoundError")
    except FileNotFoundError:
        # Expected: reading a reference that does not exist must raise FileNotFoundError.
        pass

@testbase.attach.parameter(fsbackend_trace_storage, identifier='storage')
def test_list_references(storage: FilesystemTraceStorage):
    # clear previously created refs for isolated testing
    for existing in storage.list_references():
        storage.delete(existing)

    ref1 = storage.write(b"data1", "session_1")
    final_ref1 = storage.finalize(ref1)

    ref2 = storage.write(b"data2", "session_2")
    final_ref2 = storage.finalize(ref2)

    refs = storage.list_references()
    testbase.assert_equal(len(refs), 2)
    testbase.assert_true(final_ref1 in refs)
    testbase.assert_true(final_ref2 in refs)

@testbase.attach.parameter(fsbackend_trace_storage, identifier='storage')
def test_delete_removes_data(storage: FilesystemTraceStorage):
    ref = storage.write(b"data", "session_del")
    final_ref = storage.finalize(ref)

    testbase.assert_true(storage.exists(final_ref))
    testbase.assert_true(storage.delete(final_ref))
    testbase.assert_false(storage.exists(final_ref))

@testbase.attach.parameter(fsbackend_trace_storage, identifier='storage')
def test_list_expired(storage: FilesystemTraceStorage):
    import time
    ref1 = storage.write(b"old", "session_old")
    final_ref1 = storage.finalize(ref1)

    # Touch file to be old
    old_time = time.time() - 86400 * 2 # 2 days ago
    os.utime(final_ref1, (old_time, old_time))

    ref2 = storage.write(b"new", "session_new")
    storage.finalize(ref2)

    cutoff = datetime.datetime.now() - datetime.timedelta(days=1)
    expired = storage.list_expired(cutoff)

    testbase.assert_equal(len(expired), 1)
    testbase.assert_true(final_ref1 in expired)

if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
