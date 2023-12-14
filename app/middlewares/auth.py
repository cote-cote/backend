from typing import Annotated, Union

from fastapi import Depends, Header, Security
from fastapi.security import HTTPBearer, APIKeyHeader
from pydantic import BaseModel
from starlette.requests import Request

from app.exceptions import UnauthorizedException, BadRequestException
from app.exceptions.error_code import ErrorCode
from app.utils.jwt import JwtUtil
from app.utils.redis_client import RedisClient, get_redis


authorization_header = APIKeyHeader(name="Authorization")

class UserInfo(BaseModel):
    user_id: str
    user_name: str
    user_email: str


def authenticate_request(
        request: Request,
        authorization: str = Security(authorization_header),
        redis_client: RedisClient = Depends(get_redis),
        jwt_util: JwtUtil = Depends()
) -> UserInfo:
    token = request.cookies.get("token")
    if not token:
        token = authorization
        if not token:
            raise UnauthorizedException(
                message="Either `Authorization` header or `token` cookie must be provided!",
                error_code=ErrorCode.TOKEN_NOT_PROVIDED
            )
        token = authorization.split()[-1]

    with redis_client.get_session() as redis:
        access_token = redis.get(name=token)

    if not access_token:
        raise BadRequestException(
            message="Invalid token is provided!",
            error_code=ErrorCode.INVALID_TOKEN_PROVIDED
        )

    data = jwt_util.decode(token=token)["data"]
    return UserInfo(
        user_id=data["user_id"],
        user_name=data["user_name"],
        user_email=data["user_email"]
    )
