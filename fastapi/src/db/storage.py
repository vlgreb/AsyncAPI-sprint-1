from abc import ABC, abstractmethod

from aioredis import Redis
from core.config import CACHE_EXPIRE_IN_SECONDS


class BaseStorage(ABC):
    @abstractmethod
    def save(self, key, value):
        """Сохранить запись в постоянное хранилище"""
        pass

    @abstractmethod
    def get(self, key: str):
        """Получить запись из постоянного хранилища"""
        pass

    @abstractmethod
    def delete(self, key):
        """Очистить кэш по ключу."""
        pass


class RedisStorage(BaseStorage):
    def __init__(self, redis_adapter: Redis):
        self.expire_time_sec = CACHE_EXPIRE_IN_SECONDS
        self.redis_adapter = redis_adapter

    async def save(self, key: str, value) -> None:
        """
        Сохранить запись в кэше Redis
        :param key: ключ, по которому будет храниться значение в кэше
        :param value: значение, которое запишется в кэш по данному ключу
        :return:
        """
        await self.redis_adapter.set(key, value, expire=self.expire_time_sec)

    async def get(self, key: str):
        """
        Получить запись из кэша Redis
        :param key: ключ, по которому будет храниться значение в кэше
        :return:
        """
        return await self.redis_adapter.get(key)

    async def delete(self, key):
        """Очистить кэш по ключу"""
        await self.redis_adapter.delete(key)
