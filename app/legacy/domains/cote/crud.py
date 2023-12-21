from datetime import datetime

from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.legacy.db import get_db
from app.legacy.db.models import Cote
from app.legacy.exceptions import BadRequestException
from app.legacy.exceptions.error_code import ErrorCode


class CoteCrud:

    def __init__(
            self,
            db: Session = Depends(get_db)
    ):
        self.db = db

    def find_cotes(self, page: int, per_page: int) -> list[Cote]:
        cotes = self.db.query(Cote).limit(per_page).offset((page - 1) * per_page).all()
        return cotes

    def find_cote_by_id(self, cote_id: str) -> Cote:
        try:
            cote = self.db.query(Cote).filter(Cote.id == cote_id).one()
        except NoResultFound:
            raise BadRequestException(
                message=f"No cote exists: cote_id: {cote_id}",
                error_code=ErrorCode.COTE_NOT_EXISTS
            )
        return cote

    def create_cote(self, name: str, owner_id: str, problem_url: str, capacity: int) -> Cote:
        cote = Cote(
            name=name,
            owner_id=owner_id,
            problem_url=problem_url,
            capacity=capacity
        )
        self.db.add(cote)
        return cote

    def update_cote(self, cote: Cote, kwargs: dict[str, any]) -> Cote:
        for name, value in kwargs.items():
            if value is not None and hasattr(cote, name):
                setattr(cote, name, value)
        cote.updated_at = datetime.now()
        return cote

    def delete(self, cote: Cote) -> bool:
        self.db.delete(cote)
        return True
