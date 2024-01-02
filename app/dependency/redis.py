import redis
from fastapi import Depends

from app.configs import Settings, get_settings


class Singleton(type):
    """
    An metaclass for singleton purpose. Every singleton class should inherit from this class by 'metaclass=Singleton'.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisClient(metaclass=Singleton):
    def __init__(
            self,
            host: str,
            port: int,
            password: str,
            db: int = 0
    ):
        self.connection_pool = redis.ConnectionPool(
            host=host,
            port=port,
            password=password,
            db=db
        )

    def get_session(self) -> redis.Redis:
        return redis.Redis(connection_pool=self.connection_pool)


def get_redis(settings: Settings = Depends(get_settings)) -> RedisClient:
    return RedisClient(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD
    )
