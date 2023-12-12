from datetime import datetime, timedelta

import jwt
from fastapi import Depends
from jwt import InvalidSignatureError

from app.configs import Settings, get_settings
from app.db.models import User
from app.domains.user import response


class JwtUtil:
    def __init__(
            self,
            settings: Settings = Depends(get_settings),
    ):
        self.settings = settings

    def encode_user(self, user: User) -> response.Token:
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "iat": datetime.utcnow(),
            "data": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }
        return jwt.encode(payload=payload, key=self.settings.JWT_SECRET, algorithm="HS256")

    def decode(self, token: str) -> dict[str, any]:
        try:
            payload = jwt.decode(token, self.settings.JWT_SECRET, algorithms=["HS256"])
            return payload
        except InvalidSignatureError:
            raise Exception("Invalid token has been provided")
