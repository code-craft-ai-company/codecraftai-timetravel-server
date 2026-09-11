"""
    .. module:: ccai.testshared.factories.timetravelserver.memorydatabase
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Resource factory providing a fresh in-memory SQLite database per test.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

import ccai.testbase as testbase

from ccai.timetravelserver.persistence.models.base import Base


class MemoryDatabase:
    """
        Bundles the co-dependent database objects that the registration, debug control
        and similar tests need to share: one engine, the session factory bound to it, and
        one already-open session.  Everything created from the bundle sees the same
        in-memory database.
    """

    def __init__(self, engine: Engine, session_factory: sessionmaker, session: Session):
        """
            :param engine: The SQLAlchemy engine bound to the in-memory database.
            :param session_factory: A ``sessionmaker`` bound to ``engine``.
            :param session: An open session created from ``session_factory``.
        """
        self.engine = engine
        self.session_factory = session_factory
        self.session = session
        return


@testbase.register.resource_factory()
def create_memory_database() -> Generator[MemoryDatabase, None, None]:
    """
        Creates an in-memory SQLite database with the server schema applied and yields a
        :class:`MemoryDatabase` bundle for it.  The session is closed and the engine
        disposed when the test completes.

        :returns: A generator yielding the :class:`MemoryDatabase` bundle.
    """
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    database = MemoryDatabase(engine, session_factory, session)

    yield database

    session.close()
    engine.dispose()
    return
