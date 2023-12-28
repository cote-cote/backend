import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.adapter.incoming.web import user
from app.configs import get_settings, Settings


def create_app(_settings: Settings = get_settings()) -> FastAPI:
    _app = FastAPI()
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=_settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    _app.include_router(router=user.router, prefix='/users', tags=['users'])
    return _app


app = create_app()

if __name__ == '__main__':
    settings = get_settings()
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
