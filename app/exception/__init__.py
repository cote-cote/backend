from http import HTTPStatus

from fastapi import HTTPException


class BaseRequestException:
    pass


# 400
class BadRequestException(HTTPException, BaseRequestException):
    def __init__(self, message: str, error_code: int):
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=message)
        self.message = message
        self.error_code = error_code


# 401
class UnauthorizedException(HTTPException, BaseRequestException):
    def __init__(self, message: str, error_code: int):
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED, detail=message)
        self.message = message
        self.error_code = error_code


# 403
class ForbiddenException(HTTPException, BaseRequestException):
    def __init__(self, message: str, error_code: int):
        super().__init__(status_code=HTTPStatus.FORBIDDEN, detail=message)
        self.message = message
        self.error_code = error_code


# 404
class NotFoundException(HTTPException, BaseRequestException):
    def __init__(self, message: str, error_code: int):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=message)
        self.message = message
        self.error_code = error_code
