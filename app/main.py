import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.adapter.incoming.web import user, test, cote
from app.configs import get_settings, Settings
from app.exception import BadRequestException, NotFoundException, UnauthorizedException, ForbiddenException
from app.exception.handler import bad_request_exception_handler, not_found_exception_handler, \
    unauthorized_exception_handler, forbidden_exception_handler


def create_app(_settings: Settings = get_settings()) -> FastAPI:
    _app = FastAPI()
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=_settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    _app.add_exception_handler(BadRequestException, bad_request_exception_handler)
    _app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
    _app.add_exception_handler(ForbiddenException, forbidden_exception_handler)
    _app.add_exception_handler(NotFoundException, not_found_exception_handler)

    _app.include_router(router=test.router, prefix='/test', tags=['test'])
    _app.include_router(router=user.router, prefix='/users', tags=['users'])
    _app.include_router(router=cote.router, prefix='/cotes', tags=['cotes'])
    return _app


app = create_app()

if __name__ == '__main__':
    settings = get_settings()
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
