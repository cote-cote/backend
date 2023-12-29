class BaseRequestException(Exception):
    def __init__(self, message: str, error_code: int):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class BadRequestException(BaseRequestException):
    # 400
    pass


class UnauthorizedException(BaseRequestException):
    # 401
    pass


class ForbiddenException(BaseRequestException):
    # 403
    pass


class NotFoundException(BaseRequestException):
    # 404
    pass
