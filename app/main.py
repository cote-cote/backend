import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.configs import get_settings, Settings
from app.domains.cote.router import router as cote_router
from app.domains.test.router import router as test_router
from app.domains.user.router import router as user_router


def create_app(settings: Settings = get_settings()) -> FastAPI:
    _app = FastAPI()
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    _app.include_router(router=test_router, prefix='/test', tags=['test'])
    _app.include_router(router=user_router, prefix='/users', tags=['users'])
    _app.include_router(router=cote_router, prefix='/cotes', tags=['cotes'])
    return _app


app = create_app()

if __name__ == '__main__':
    settings = get_settings()
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
