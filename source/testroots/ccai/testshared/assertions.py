"""
    .. module:: ccai.testshared.assertions
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Assertion helpers shared by the testbase tests in this repository.
"""

import re

from contextlib import contextmanager
from typing import Iterator, Optional, Tuple, Type, Union

ExpectedExceptions = Union[Type[BaseException], Tuple[Type[BaseException], ...]]


class RaisedExceptionCapture:
    """
        Holds the exception captured by :func:`assert_raises` so a test can inspect it
        after the ``with`` block has completed.
    """

    def __init__(self):
        self.exception: Optional[BaseException] = None
        return


@contextmanager
def assert_raises(expected: ExpectedExceptions, match: Optional[str] = None) -> Iterator[RaisedExceptionCapture]:
    """
        Context manager that asserts the body raises an exception of the expected type.

        The expected exception is swallowed and made available on the yielded capture
        object.  Any other exception propagates untouched.  If the body completes without
        raising, an :class:`AssertionError` is raised.

        :param expected: The exception type, or tuple of types, that the body must raise.
        :param match: Optional regular expression that must be found (``re.search``) in
                      the string form of the raised exception.

        :returns: A :class:`RaisedExceptionCapture` whose ``exception`` attribute is set
                  once the body has raised.
    """
    capture = RaisedExceptionCapture()

    try:
        yield capture
    except expected as raised:
        capture.exception = raised
        if match is not None:
            message = str(raised)
            if re.search(match, message) is None:
                errmsg = f"Raised {type(raised).__name__}({message!r}) does not match pattern {match!r}."
                raise AssertionError(errmsg) from raised
        return

    if isinstance(expected, tuple):
        names = ", ".join(exc_type.__name__ for exc_type in expected)
    else:
        names = expected.__name__

    raise AssertionError(f"Expected an exception of type ({names}) to be raised but no exception was raised.")
