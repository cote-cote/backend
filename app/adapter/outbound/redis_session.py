from typing import Union

from fastapi import Depends

from app.application.port.outbound.session import SessionPort
from app.dependency.redis import RedisClient, get_redis


class RedisSessionAdapter(SessionPort):

    def __init__(self, redis: RedisClient = Depends(get_redis)):
        self.redis = redis

    def get(self, key: str) -> any:
        with self.redis.get_session() as redis:
            return redis.get(name=key)

    def put(self, key: str, value: Union[str, int, bool]) -> bool:
        with self.redis.get_session() as redis:
            redis.set(name=key, value=value)
        return True
