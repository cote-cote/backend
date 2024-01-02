from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.adapter.incoming.web.schema.request.user_authorization import UserAuthorization
from app.port.incoming.oauth_signin_use_case import OauthSignInUseCase
from app.configs import Settings, get_settings
from app.dependency.oauth_service import get_oauth_sign_in_service

router = APIRouter()


@router.post("/oauth/authorization/{oauth_provider_name}")
def authorize_user(
        request_body: UserAuthorization,
        response: Response,
        sign_in_use_case: OauthSignInUseCase = Depends(get_oauth_sign_in_service),
        settings: Settings = Depends(get_settings)
) -> dict[str, str]:
    user_token = sign_in_use_case.sign_in(auth_code=request_body.auth_code)

    response.set_cookie(
        key="user_token",
        value=user_token,
        httponly=True if settings.ENV == 'prod' else False,
        secure=True if settings.ENV == 'prod' else False
    )
    return {"user_token": user_token}
