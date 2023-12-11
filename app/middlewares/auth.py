from fastapi import Depends
from starlette.requests import Request

from app.utils.jwt import JwtUtil


def authenticate_token_cookie(
        request: Request,
        jwt_util: JwtUtil = Depends()
) -> dict[str, any]:
    token = request.cookies.get("token")
    if not token:
        raise Exception("No token in the cookie!")
    payload = jwt_util.decode(token=token)
    return payload
