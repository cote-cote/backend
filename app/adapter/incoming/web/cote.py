from http import HTTPStatus

from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.adapter.incoming.web.schema.request.cote import CoteReadRequest, CoteCreateRequest, CoteUpdateRequest
from app.adapter.incoming.web.schema.response.cote import CoteResponse
from app.adapter.outbound.token import TokenAdapter
from app.application.domain.service.cote_crud_service import CoteCrudService
from app.application.port.incoming.cote.crud_use_case import CoteCrudUseCase
from app.application.port.outbound.token import TokenPort
from app.dependency.auth import authenticate_request, UserToken

router = APIRouter()


@router.get("")
def get_cotes(
        cote_read_request: CoteReadRequest = Depends(),
        cote_crud_use_case: CoteCrudUseCase = Depends(CoteCrudService)
) -> list[CoteResponse]:
    cotes = cote_crud_use_case.get_cotes(cote_read=cote_read_request.to_cote_read())
    return cotes


@router.get("/{cote_id}")
def get_cote(
        cote_id: str,
        user_token: UserToken = Depends(authenticate_request),
        cote_crud_use_case: CoteCrudUseCase = Depends(CoteCrudService)
) -> CoteResponse:
    cote = cote_crud_use_case.get_cote(cote_id=cote_id)
    return cote


@router.post("")
def create_cote(
        cote_create_request: CoteCreateRequest,
        user_token: UserToken = Depends(authenticate_request),
        cote_crud_use_case: CoteCrudUseCase = Depends(CoteCrudService),
        token_port: TokenPort = Depends(TokenAdapter)
) -> CoteResponse:
    user_id = token_port.get_user_id(token=user_token.value)
    cote = cote_crud_use_case.create_cote(
        cote_create=cote_create_request.to_cote_create(owner_id=user_id)
    )
    return cote


@router.patch("/{cote_id}")
def modify_cote(
        cote_id: str,
        cote_update_request: CoteUpdateRequest,
        user_token: UserToken = Depends(authenticate_request),
        cote_crud_use_case: CoteCrudUseCase = Depends(CoteCrudService),
        token_port: TokenPort = Depends(TokenAdapter)
) -> CoteResponse:
    user_id = token_port.get_user_id(token=user_token.value)
    modified_cote = cote_crud_use_case.update_cote(
        cote_id=cote_id,
        user_id=user_id,
        cote_update=cote_update_request.to_cote_update()
    )
    return modified_cote


@router.delete("/{cote_id}")
def delete_cote(
        cote_id: str,
        user_token: UserToken = Depends(authenticate_request),
        cote_crud_use_case: CoteCrudUseCase = Depends(CoteCrudService),
        token_port: TokenPort = Depends(TokenAdapter)
):
    user_id = token_port.get_user_id(token=user_token.value)
    cote_crud_use_case.delete_cote(cote_id=cote_id, user_id=user_id)
    return Response(status_code=HTTPStatus.NO_CONTENT)
