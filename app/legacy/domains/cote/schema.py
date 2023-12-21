from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel

from app.legacy.exceptions import BadRequestException
from app.legacy.exceptions.error_code import ErrorCode


class CoteReadRequest:
    def __init__(
            self,
            page: int = Query(default=1, description='<p><b>조회 할 페이지</b><p>'
                                                     '<p>페이지는 1부터 시작</p>'),
            per_page: int = Query(default=10, description='한 페이지 당 보여줄 게시글의 갯수')
    ):
        if page < 1:
            raise BadRequestException(
                message="page must be greater than 0",
                error_code=ErrorCode.WRONG_PAGE_NUMBER_PROVIDED
            )
        elif per_page < 1 or per_page > 100:
            raise BadRequestException(
                message="per_page must be greater than 0 and less than 100",
                error_code=ErrorCode.WRONG_PER_PAGE_NUMBER_PROVIDED
            )

        self.page = page
        self.per_page = per_page


class CoteCreateRequest(BaseModel):
    name: str
    problem_url: str
    capacity: int


class CoteModifyRequest(BaseModel):
    name: Optional[str] = None
    owner_id: Optional[str] = None
    capacity: Optional[int] = None


class CoteResponse(BaseModel):
    cote_id: str
    cote_name: str
    cote_problem_url: str
    cote_capacity: int
    cote_created_date: datetime
    cote_updated_date: datetime
