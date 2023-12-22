from datetime import datetime, timedelta

import jwt
from fastapi import Depends
from jwt import InvalidSignatureError

from app.configs import Settings, get_settings


class JwtUtil:
    def __init__(
            self,
            settings: Settings = Depends(get_settings),
    ):
        self.settings = settings

    def encode(self, payload: dict[str, any]) -> str:
        _payload = {
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "iat": datetime.utcnow(),
            "data": payload
        }
        return jwt.encode(payload=_payload, key=self.settings.JWT_SECRET, algorithm="HS256")

    def decode(self, token: str) -> dict[str, any]:
        try:
            payload = jwt.decode(token, self.settings.JWT_SECRET, algorithms=["HS256"])
            return payload
        except InvalidSignatureError:
            raise Exception("Invalid token has been provided")
