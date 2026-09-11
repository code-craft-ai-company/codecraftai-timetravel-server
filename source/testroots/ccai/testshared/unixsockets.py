"""
    .. module:: ccai.testshared.unixsockets
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Helpers for tests that bind Unix domain sockets.
"""

import shutil
import socket
import tempfile

from contextlib import contextmanager
from typing import Iterator

from ccai.errors.exceptions import SkipError


def require_unix_domain_sockets():
    """
        Skips the calling test when the platform does not provide Unix domain sockets.

        Unix domain sockets do not exist on Windows: ``socket.AF_UNIX`` is absent there,
        so a test that needs to bind one skips rather than failing inside the receiver.
        The product modules themselves import cleanly on Windows; only binding needs
        ``AF_UNIX``, which is why the guard belongs on the tests and not on the import.
    """
    if not hasattr(socket, "AF_UNIX"):
        raise SkipError(reason="Unix domain sockets (socket.AF_UNIX) are not available on this platform")
    return


@contextmanager
def temporary_socket_directory() -> Iterator[str]:
    """
        Yields a SHORT temporary directory suitable for Unix socket paths and removes it
        on exit.

        AF_UNIX caps a socket path near 104 bytes on macOS.  A per-test directory derived
        from the test NAME can push socket paths over the limit for the longer-named tests,
        which then fail with 'AF_UNIX path too long' while the shorter-named ones pass.
        That looks like a receiver bug rather than a path-length one, and it only starts
        happening when the repository moves to a deeper directory.

        mkdtemp under the system temp root is short and name-independent, so the limit
        cannot be reached by renaming a test.
    """
    path = tempfile.mkdtemp(prefix='ttr')
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)
