from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.configs import get_settings, Settings
from app.domains.user import request
from app.domains.user.service import UserService

router = APIRouter()


@router.post("/sign-up")
def register_user(
        request_body: request.UserSignUp,
        user_service: UserService = Depends()
):
    created_user = user_service.register_user(request_body=request_body)
    return created_user


@router.post("/sign-in")
def sign_in(
        response: Response,
        request_body: request.UserSignin,
        user_service: UserService = Depends(),
        settings: Settings = Depends(get_settings)
):
    token = user_service.sign_in(request_body=request_body)
    response.set_cookie(
        key="token",
        value=token.value,
        httponly=True if settings.ENV == 'prod' else False,
        secure=True if settings.ENV == 'prod' else False
    )
    return token


@router.post("/sign-out")
def sign_out(
        response: Response
) -> str:
    response.delete_cookie("token")
    return "Signed out!"
