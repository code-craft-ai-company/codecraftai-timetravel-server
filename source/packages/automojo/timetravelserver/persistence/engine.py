from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

def create_db_engine(database_url: str):
    return create_engine(database_url)

def create_session_factory(engine):
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
