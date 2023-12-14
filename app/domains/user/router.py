from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.configs import get_settings, Settings
from app.domains.user.schema import RequestUserAuthorization
from app.domains.user.service import UserService

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
