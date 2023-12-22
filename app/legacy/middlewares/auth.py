from fastapi import Depends, Security
from fastapi.security import APIKeyHeader
from starlette.requests import Request

from app.legacy.domains import UserInfo
from app.legacy.exceptions import UnauthorizedException, BadRequestException
from app.legacy.exceptions import ErrorCode
from app.legacy.utils.jwt import JwtUtil
from app.legacy.utils.redis_client import RedisClient, get_redis

authorization_header = APIKeyHeader(name="Authorization",auto_error=False)


def authenticate_request(
        request: Request,
        authorization: str = Security(authorization_header),
        redis_client: RedisClient = Depends(get_redis),
        jwt_util: JwtUtil = Depends()
) -> UserInfo:
    token = request.cookies.get("user_token")
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
        user_email=data["user_email"],
        user_token=token,
        access_token=access_token
    )