from fastapi import Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from starlette.requests import Request

from app.adapter.outbound.redis_session import RedisSessionAdapter
from app.application.port.outbound.session import SessionPort
from app.exception import UnauthorizedException, BadRequestException
from app.exception.error_code import ErrorCode

authorization_header = APIKeyHeader(name="Authorization", auto_error=False)


class UserToken(BaseModel):
    value: str


def authenticate_request(
        request: Request,
        authorization: str = Security(authorization_header),
        session_port: SessionPort = Depends(RedisSessionAdapter)
) -> UserToken:
    token = request.cookies.get("user_token")
    if not token:
        token = authorization
        if not token:
            raise UnauthorizedException(
                message="Either `Authorization` header or `token` cookie must be provided!",
                error_code=ErrorCode.TOKEN_NOT_PROVIDED
            )
        token = authorization.split()[-1]

    access_token = session_port.get(key=token)
    if not access_token:
        raise BadRequestException(
            message="Invalid token is provided!",
            error_code=ErrorCode.INVALID_TOKEN_PROVIDED
        )

    return UserToken(
        value=token
    )
