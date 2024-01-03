from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeMeta, Session

from app.domain.entity import Base, User
from app.dependency.db import get_engine, get_db


class TestingHelper:
    def __init__(
            self,
            db: Session = Depends(get_db),
            engine: Engine = Depends(get_engine)
    ):
        self.db = db
        self.engine = engine

    def generate_tables(self, base: Base, models: list[DeclarativeMeta]):
        tables = []
        for model in models:
            tables.append(model.__table__)

        base.metadata.create_all(bind=self.engine, tables=tables, checkfirst=True)

    def create_dummy_user_data(self, n: int = 10) -> list[User]:
        users = [
            User(
                name=f"user_{i}",
                email=f"email{i}@test.com"
            ) for i in range(n)
        ]
        self.db.add_all(users)
        self.db.commit()
        return users
