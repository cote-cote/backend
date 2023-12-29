from datetime import datetime

from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.application.entity import Cote
from app.application.port.incoming.cote.crud_use_case import CoteUpdate, CoteCreate
from app.application.port.outbound.cote_crud import CoteCrudPort
from app.dependency.db import get_db
from app.exception import BadRequestException
from app.exception.error_code import ErrorCode


class CoteCrudAdapter(CoteCrudPort):
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

    def create_cote(self, cote_create: CoteCreate) -> Cote:
        cote = Cote(
            name=cote_create.name,
            owner_id=cote_create.owner_id,
            problem_url=cote_create.problem_url,
            capacity=cote_create.capacity
        )
        self.db.add(cote)
        return cote

    def update_cote(self, cote: Cote, cote_update: CoteUpdate) -> Cote:
        for name, value in cote_update.model_dump().items():
            if value is not None and hasattr(cote, name):
                setattr(cote, name, value)
        cote.updated_at = datetime.now()
        return cote

    def delete_cote(self, cote: Cote) -> bool:
        self.db.delete(cote)
        return True

    def commit(self) -> bool:
        self.db.commit()
        return True
