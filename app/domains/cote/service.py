from fastapi import Depends
from sqlalchemy.orm import Session

from app.configs import Settings, get_settings
from app.db import get_db
from app.domains.cote.crud import CoteCrud
from app.domains.cote.schema import CoteResponse, CoteReadRequest, CoteCreateRequest, CoteModifyRequest
from app.domains.oauth import UserInfo
from app.exceptions import ForbiddenException
from app.exceptions.error_code import ErrorCode
from app.utils.jwt import JwtUtil
from app.utils.redis_client import RedisClient, get_redis


class CoteService:

    def __init__(
            self,
            db: Session = Depends(get_db),
            settings: Settings = Depends(get_settings),
            cote_crud: CoteCrud = Depends(),
            jwt_util: JwtUtil = Depends(),
            redis_client: RedisClient = Depends(get_redis)
    ):
        self.db = db
        self.settings = settings
        self.cote_crud = cote_crud
        self.jwt_util = jwt_util
        self.redis_client = redis_client

    def get_cotes(self, request_param: CoteReadRequest) -> list[CoteResponse]:
        cotes = self.cote_crud.find_cotes(page=request_param.page, per_page=request_param.per_page)
        return [
            CoteResponse(
                cote_id=cote.id,
                cote_name=cote.name,
                cote_capacity=cote.capacity,
                cote_created_date=cote.created_at
            ) for cote in cotes
        ]

    def create_cote(self, user_info: UserInfo, request_body: CoteCreateRequest) -> CoteResponse:
        cote = self.cote_crud.create_cote(
            name=request_body.name,
            owner_id=user_info.user_id,
            problem_url=request_body.problem_url,
            capacity=request_body.capacity
        )

        self.db.commit()
        return CoteResponse(
            cote_id=cote.id,
            cote_name=cote.name,
            cote_capacity=cote.capacity,
            cote_problem_url=cote.problem_url,
            cote_created_date=cote.created_at,
            cote_updated_date=cote.updated_at
        )

    def modify_cote(
            self,
            cote_id: str,
            user_info: UserInfo,
            request_body: CoteModifyRequest,
    ) -> CoteResponse:
        with self.redis_client.get_session() as redis:
            lock = redis.lock(
                name=f"cote_{cote_id}",
                timeout=self.settings.REDIS_LOCK_TIMEOUT,
                blocking_timeout=self.settings.REDIS_BLOCKING_TIMEOUT
            )

            with lock:
                cote = self.cote_crud.find_cote_by_id(cote_id=cote_id)

                if cote.owner_id != user_info.user_id:
                    raise ForbiddenException(
                        message=f"This user_id is not authorized: {user_info.user_id}",
                        error_code=ErrorCode.WRONG_OWNER_ID
                    )

                self.cote_crud.update_cote(cote=cote, kwargs=request_body.model_dump())
                self.db.commit()

        return CoteResponse(
            cote_id=cote.id,
            cote_name=cote.name,
            cote_capacity=cote.capacity,
            cote_problem_url=cote.problem_url,
            cote_created_date=cote.created_at,
            cote_updated_date=cote.updated_at
        )

    def delete_cote(self, cote_id: str, user_info: UserInfo) -> None:
        cote = self.cote_crud.find_cote_by_id(cote_id=cote_id)
        if cote.owner_id != user_info.user_id:
            raise ForbiddenException(
                message=f"This user_id is not authorized: {user_info.user_id}",
                error_code=ErrorCode.WRONG_OWNER_ID
            )

        self.cote_crud.delete(cote)
        self.db.commit()
