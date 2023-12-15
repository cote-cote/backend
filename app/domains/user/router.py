from http import HTTPStatus

from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.configs import get_settings, Settings
from app.domains.oauth import UserInfo
from app.domains.user.schema import RequestUserAuthorization
from app.domains.user.service import UserService
from app.middlewares.auth import authenticate_request

router = APIRouter()


@router.post("/oauth/authorization")
def authorize_user(
        request_body: RequestUserAuthorization,
        response: Response,
        user_service: UserService = Depends(),
        settings: Settings = Depends(get_settings)
) -> dict[str, str]:
    token = user_service.authorize(request_body=request_body)
    response.set_cookie(
        key="access_token",
        value=token.value,
        httponly=True if settings.ENV == 'prod' else False,
        secure=True if settings.ENV == 'prod' else False
    )
    return {"token": token.value}


@router.post("/sign-out")
def sign_out(
        response: Response,
        user_info: UserInfo = Depends(authenticate_request),
        user_service: UserService = Depends()
):
    user_service.delete_user_session(user_info=user_info)
    response.delete_cookie("access_token")
    return Response(status_code=HTTPStatus.NO_CONTENT)
