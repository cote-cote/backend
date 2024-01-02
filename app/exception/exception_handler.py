from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.exception import BadRequestException, NotFoundException, UnauthorizedException, ForbiddenException


async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.message, "error_code": exc.error_code}
    )


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exc.message, "error_code": exc.error_code}
    )


async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": exc.message, "error_code": exc.error_code}
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message, "error_code": exc.error_code}
    )
