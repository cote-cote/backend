from datetime import timedelta

import requests
from fastapi import Depends
from sqlalchemy.orm import Session

from app.configs import get_settings, Settings
from app.db import get_db
from app.db.models import User
from app.domains.user.crud import UserCrud
from app.domains.user.schema import RequestUserAuthorization, Token
from app.exceptions import BadRequestException
from app.utils.jwt import JwtUtil
from app.utils.password import PasswordUtil
from app.utils.redis_client import get_redis, RedisClient


class UserService:

    def __init__(
            self,
            db: Session = Depends(get_db),
            user_crud: UserCrud = Depends(),
            settings: Settings = Depends(get_settings),
            redis: RedisClient = Depends(get_redis),
            password_util: PasswordUtil = Depends(),
            jwt_util: JwtUtil = Depends()
    ):
        self.db = db
        self.user_crud = user_crud
        self.settings = settings
        self.redis = redis
        self.password_util = password_util
        self.jwt_util = jwt_util

    def _get_access_token(self, auth_code: str) -> str:
        response = requests.post(
            url="https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": self.settings.GITHUB_CLIENT_ID,
                "client_secret": self.settings.GITHUB_CLIENT_SECRET,
                "code": auth_code
            }
        )
        result = response.json()
        access_token = result["access_token"]

        return access_token

    def _get_user_info(self, access_token: str) -> str:
        response = requests.get(
            url=f"{self.settings.GITHUB_API_BASE_URL}/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
        )
        result = response.json()
        return result

    def _get_user_email(self, access_token: str) -> str:
        response = requests.get(
            url=f"{self.settings.GITHUB_API_BASE_URL}/user/emails",
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
        )
        result = response.json()
        email = result[0]['email']
        return email

    def authorize(self, request_body: RequestUserAuthorization) -> Token:
        access_token = self._get_access_token(auth_code=request_body.auth_code)

        user_info = self._get_user_info(access_token=access_token)
        email = self._get_user_email(access_token=access_token)

        try:
            user = self.user_crud.find_user_by_email(email=email)
        except BadRequestException:
            user = User(name=user_info["name"], email=email)
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
