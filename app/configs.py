import os
from typing import Optional

from pydantic.v1 import BaseSettings

CURRENT_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.abspath(os.path.join(CURRENT_PATH, '..'))


class Settings(BaseSettings):
    """
        Set environment variables to use these settings or put `local.env` file on the project root path
    """
    ENV: str = 'dev'  # dev, stg, prod, etc.
    HOST: str = None
    PORT: int = 8000

    ALLOWED_ORIGINS: list[str] = []

    DB_DRIVER: str = "mysql+mysqldb"
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: Optional[str]
    REDIS_TTL_SEC: int = 8 * 60 * 60
    REDIS_LOCK_TIMEOUT: int = 5
    REDIS_BLOCKING_TIMEOUT: int = 10

    JWT_SECRET: str = "SECRET_KEY"

    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str

    @property
    def DB_URL(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


def get_settings():
    return Settings(_env_file=f'{ROOT_PATH}/local.env', _env_file_encoding='utf-8')
