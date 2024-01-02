import contextlib

from fastapi import Depends

from app.application.port.outbound.concurrency_port import ConcurrencyPort
from app.configs import get_settings, Settings
from app.dependency.redis import RedisClient, get_redis


class RedisConcurrencyAdapter(ConcurrencyPort):

    def __init__(
            self,
            redis: RedisClient = Depends(get_redis),
            settings: Settings = Depends(get_settings)
    ):
        self.redis = redis
        self.settings = settings

    @contextlib.contextmanager
    def lock(self, key: str) -> None:
        with self.redis.get_session() as redis:
            lock = redis.lock(
                name=key,
                timeout=self.settings.REDIS_LOCK_TIMEOUT,
                blocking_timeout=self.settings.REDIS_BLOCKING_TIMEOUT
            )
            with lock:
                yield lock
