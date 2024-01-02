from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeMeta

from app.application.entity import Base
from app.dependency.db import get_engine


class TestingHelper:
    def __init__(
            self,
            engine: Engine = Depends(get_engine)
    ):
        self.engine = engine

    def generate_tables(self, base: Base, models: list[DeclarativeMeta]):
        tables = []
        for model in models:
            tables.append(model.__table__)

        base.metadata.create_all(bind=self.engine, tables=tables, checkfirst=True)
