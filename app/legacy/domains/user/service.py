from datetime import timedelta

from fastapi import Depends
from sqlalchemy.orm import Session

from app.configs import get_settings, Settings
from app.legacy.db import get_db
from app.legacy.db.models import User
from app.legacy.domains.oauth import OauthProvider
from app.legacy.domains.oauth.github import GithubOauthProvider
from app.legacy.domains.user.crud import UserCrud
from app.legacy.domains.user.schema import RequestUserAuthorization, Token
from app.legacy.exceptions import BadRequestException
from app.legacy.middlewares.auth import UserInfo
from app.legacy.utils.jwt import JwtUtil
from app.legacy.utils import PasswordUtil
from app.legacy.utils.redis_client import get_redis, RedisClient


class UserService:

    def __init__(
            self,
            db: Session = Depends(get_db),
            user_crud: UserCrud = Depends(),
            settings: Settings = Depends(get_settings),
            redis: RedisClient = Depends(get_redis),
            oauth_provider: OauthProvider = Depends(GithubOauthProvider),
            password_util: PasswordUtil = Depends(),
            jwt_util: JwtUtil = Depends()
    ):
        self.db = db
        self.user_crud = user_crud
        self.settings = settings
        self.redis = redis
        self.oauth_provider = oauth_provider
        self.password_util = password_util
        self.jwt_util = jwt_util

    def authorize(self, request_body: RequestUserAuthorization) -> Token:
        access_token = self.oauth_provider.get_access_token(auth_code=request_body.auth_code)
        user_info = self.oauth_provider.get_user_info(access_token=access_token)

        try:
            user = self.user_crud.find_user_by_email(email=user_info.user_email)
        except BadRequestException:
            user = User(name=user_info.user_name, email=user_info.user_email)
            self.user_crud.save_user(user)
            self.db.commit()

        token = self.jwt_util.encode(
            payload={
                "user_id": user.id,
                "user_name": user.name,
                "user_email": user.email
            }
        )
        with self.redis.get_session() as redis:
            redis.set(token, access_token, timedelta(seconds=self.settings.REDIS_TTL_SEC))

        return Token(value=token)

    def delete_user_session(self, user_info: UserInfo) -> bool:
        with self.redis.get_session() as redis:
            redis.delete(user_info.user_token)

        return True
