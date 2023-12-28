from fastapi import Depends

from app.adapter.outbound.github_oauth import GithubOauthAdapter
from app.adapter.outbound.redis_session import RedisSessionAdapter
from app.adapter.outbound.token import TokenAdapter
from app.adapter.outbound.user_create import UserCreateAdapter
from app.application.port.incoming.oauth_signin_use_case import OauthSignInUseCase, UserInfo
from app.application.port.outbound.oauth import OauthPort
from app.application.port.outbound.session import SessionPort
from app.application.port.outbound.token import TokenPort
from app.application.port.outbound.user_create import UserCreatePort


class GithubOauthSignInService(OauthSignInUseCase):
    def __init__(
            self,
            oauth_port: OauthPort = Depends(GithubOauthAdapter),
            session_port: SessionPort = Depends(RedisSessionAdapter),
            token_port: TokenPort = Depends(TokenAdapter),
            user_create_port: UserCreatePort = Depends(UserCreateAdapter)
    ):
        self.oauth_port = oauth_port
        self.session_port = session_port
        self.token_port = token_port
        self.user_create_port = user_create_port

    def _create_user_token(self, user_id: str, user_info: UserInfo) -> str:
        token = self.token_port.encode(
            payload={
                "user_id": user_id,
                "user_name": user_info.name,
                "user_email": user_info.email
            }
        )
        return token

    def _store_token_pair_into_session(self, user_token: str, access_token: str) -> bool:
        self.session_port.put(key=user_token, value=access_token)
        return True

    def sign_in(self, auth_code: str) -> str:
        access_token = self.oauth_port.get_oauth_access_code(auth_code=auth_code)
        user_info = self.oauth_port.get_user_info(access_token=access_token)

        user = self.user_create_port.create_if_not_exist(user_info=user_info)
        self.user_create_port.commit()

        user_token = self._create_user_token(user_id=user.id, user_info=user_info)
        self._store_token_pair_into_session(user_token=user_token, access_token=access_token)

        return user_token
