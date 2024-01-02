from functools import cache
from typing import Generator

from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.configs import get_settings


@cache
def get_engine() -> Engine:
    _settings = get_settings()
    return create_engine(_settings.DB_URL, echo=True if _settings.ENV != 'prod' else False)


@cache
def get_session_maker(engine: Engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    Session = get_session_maker(get_engine())
    with Session() as db:
        yield db
