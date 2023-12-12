import jwt
from fastapi import Depends
from sqlalchemy.orm import Session

from app.configs import get_settings, Settings
from app.db import get_db
from app.domains.user import request
from app.domains.user import response
from app.domains.user.crud import UserCrud
from app.utils.jwt import JwtUtil
from app.utils.password import PasswordUtil


class UserService:

    def __init__(
            self,
            db: Session = Depends(get_db),
            user_crud: UserCrud = Depends(),
            settings: Settings = Depends(get_settings),
            password_util: PasswordUtil = Depends(),
            jwt_util: JwtUtil = Depends()
    ):
        self.db = db
        self.user_crud = user_crud
        self.settings = settings
        self.password_util = password_util
        self.jwt_util = jwt_util

    def register_user(self, request_body: request.UserSignUp) -> response.User:
        created_user = self.user_crud.create_user(
            name=request_body.name,
            email=request_body.email,
            password=self.password_util.encrypt(request_body.password)
        )

        self.db.commit()
        return response.User(
            user_id=created_user.id,
            user_name=created_user.name,
            user_email=created_user.email
        )

    def sign_in(self, request_body: request.UserSignin) -> response.Token:
        user = self.user_crud.find_user_by_email(email=request_body.email)

        is_valid = self.password_util.check_password(request_body.password, user.password)
        if not is_valid:
            raise Exception()

        token = self.jwt_util.encode_user(user)
        return token



