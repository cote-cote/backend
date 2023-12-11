import os

from pydantic.v1 import BaseSettings

CURRENT_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.abspath(os.path.join(CURRENT_PATH, '..', '..'))


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

    JWT_SECRET: str = "SECRET_KEY"

    @property
    def DB_URL(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


def get_settings():
    return Settings(_env_file=f'{ROOT_PATH}/local.env', _env_file_encoding='utf-8')
