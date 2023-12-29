from fastapi import Depends

from app.adapter.outbound.cote_crud import CoteCrudAdapter
from app.adapter.outbound.cote_lock_key import CoteLockKeyAdapter
from app.adapter.outbound.redis_concurrency import RedisConcurrencyAdapter
from app.application.domain.model import Cote
from app.application.port.incoming.cote.crud_use_case import CoteCrudUseCase, CoteUpdate, CoteCreate, CoteRead
from app.application.port.outbound.concurrency_port import ConcurrencyPort
from app.application.port.outbound.cote_crud import CoteCrudPort
from app.application.port.outbound.cote_lock_key import CoteLockKeyPort
from app.exception import ForbiddenException
from app.exception.error_code import ErrorCode


class CoteCrudService(CoteCrudUseCase):
    def __init__(
            self,
            cote_crud_port: CoteCrudPort = Depends(CoteCrudAdapter),
            cote_lock_key_port: CoteLockKeyPort = Depends(CoteLockKeyAdapter),
            concurrency_port: ConcurrencyPort = Depends(RedisConcurrencyAdapter)
    ):
        self.cote_crud_port = cote_crud_port
        self.cote_lock_key_port = cote_lock_key_port
        self.concurrency_port = concurrency_port

    def get_cotes(self, cote_read: CoteRead) -> list[Cote]:
        cotes = self.cote_crud_port.find_cotes(page=cote_read.page, per_page=cote_read.per_page)
        return cotes

    def get_cote(self, cote_id: str) -> Cote:
        cote = self.cote_crud_port.find_cote_by_id(cote_id=cote_id)
        return cote

    def create_cote(self, cote_create: CoteCreate) -> Cote:
        cote = self.cote_crud_port.create_cote(cote_create=cote_create)
        self.cote_crud_port.commit()
        return cote

    def update_cote(self, cote_id: str, user_id: str, cote_update: CoteUpdate) -> Cote:
        key = self.cote_lock_key_port.generate_key(key_id=cote_id)
        with self.concurrency_port.lock(key=key):
            cote = self.cote_crud_port.find_cote_by_id(cote_id=cote_id)

            if cote.owner_id != user_id:
                raise ForbiddenException(
                    message=f"This user_id is not authorized: {user_id}",
                    error_code=ErrorCode.WRONG_OWNER_ID
                )
            self.cote_crud_port.update_cote(cote=cote, cote_update=cote_update)
            self.cote_crud_port.commit()

    def delete_cote(self, cote_id: str, user_id: str) -> bool:
        cote = self.cote_crud_port.find_cote_by_id(cote_id=cote_id)
        if cote.owner_id != user_id:
            raise ForbiddenException(
                message=f"This user_id is not authorized: {user_id}",
                error_code=ErrorCode.WRONG_OWNER_ID
            )

        self.cote_crud_port.delete_cote(cote)
        self.cote_crud_port.commit()

        return True
