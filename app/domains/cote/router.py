from http import HTTPStatus

from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.domains.cote.schema import CoteResponse, CoteReadRequest, CoteCreateRequest, CoteModifyRequest
from app.domains.cote.service import CoteService
from app.domains.oauth import UserInfo
from app.middlewares.auth import authenticate_request

router = APIRouter()


@router.get("")
def get_cotes(
        request_param: CoteReadRequest = Depends(),
        cote_service: CoteService = Depends()
) -> list[CoteResponse]:
    cotes = cote_service.get_cotes(request_param)
    return cotes


@router.post("")
def create_cote(
        request_body: CoteCreateRequest,
        user_info: UserInfo = Depends(authenticate_request),
        cote_service: CoteService = Depends()
) -> CoteResponse:
    cote = cote_service.create_cote(
        user_info=user_info,
        request_body=request_body
    )
    return cote


@router.patch("/{cote_id}")
def modify_cote(
        cote_id: str,
        request_body: CoteModifyRequest,
        user_info: UserInfo = Depends(authenticate_request),
        cote_service: CoteService = Depends()
) -> CoteResponse:
    modified_cote = cote_service.modify_cote(
        cote_id=cote_id,
        user_info=user_info,
        request_body=request_body
    )
    return modified_cote


@router.delete("/{cote_id}")
def delete_cote(
        cote_id: str,
        user_info: UserInfo = Depends(authenticate_request),
        cote_service: CoteService = Depends()
):
    cote_service.delete_cote(cote_id=cote_id, user_info=user_info)
    return Response(status_code=HTTPStatus.NO_CONTENT)
