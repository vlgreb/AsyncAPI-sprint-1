import logging
from typing import Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

CACHE_EXPIRE_IN_SECONDS = 60 * 5


class BaseService:
    """
    Класс представляет базовый интерфейс для работы с ElasticSearch и Redis. Получение по id (или прочему ключу)
    документов и их кеширование.
    """
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index_name: str = '', service_name: str = 'base'):
        self.redis = redis
        self.elastic = elastic
        self.index_name = index_name
        self.service_name = service_name

    async def get_by_id(self, doc_id: str) -> Optional[dict]:
        """
        Возвращает документ по ключу (id). Ищет документ по ключу doc_id в кэше Redis и,
        если не находит, обращается к ElasticSearch. Возвращает None при отсутствии в Elastic.

        :param doc_id: строка (ключ, id), по которой ищется документ
        :return: документ в виде словаря
        """
        doc = await self._get_from_cache(doc_id)
        if not doc:
            doc = await self._get_from_elastic(doc_id)
            if not doc:
                return None
            await self._put_to_cache(doc_id, doc)

        return doc

    async def _get_from_cache(self, doc_id: str) -> Optional[dict]:
        """
        Ищет документ по ключу doc_id в кэше Redis
        :param doc_id: строка (ключ, id), по которой ищется документ
        :return: документ в виде словаря
        """
        if self.redis.exists(doc_id):
            logging.info(f'[{self.service_name}] from cache by id')
            return await self.redis.get(doc_id)

    async def _put_to_cache(self, doc_id: str, doc: dict) -> None:
        """
        Сохраняет документ в кэш Redis.
        :param doc_id: строка (ключ, id), по которой в кэш записывается документ
        :param doc: словарь
        :return: None
        """
        logging.info(f'[{self.service_name}] write to cache by id')
        await self.redis.set(doc_id, orjson.dumps(doc).decode(), expire=CACHE_EXPIRE_IN_SECONDS)

    async def _get_from_elastic(self, doc_id: str) -> Optional[dict]:
        """

        :param doc_id: строка (ключ, id), по которой ищется документ
        :return: документ в виде словаря
        """
        try:
            doc = await self.elastic.get(index=self.index_name, id=doc_id)
            logging.info(f'[{self.service_name}] from elastic by id')
        except NotFoundError:
            logging.info(f'[{self.service_name}] can\'t find in elastic by id')
            return None
        return doc['_source']

    async def _get_list_of_data_from_cache(self, key: str, redis_range: int) -> Optional[list]:
        """
        Метод предназначен для получения массива (списка) данных из кэша
        :param key: ключ, по которому требуеся достать данные из кэша
        :param redis_range:
        :return: список документов
        """
        data = await self.redis.lrange(key, 0, redis_range)
        return data

    async def _put_list_of_data_to_cache(self, data: list, key: str):
        """
        Метод сохраняет в кэш массив (список) данных по ключу key.
        :param data:
        :param key:
        :return:
        """
        logging.info(f'[{self.service_name}] write film_data to cache')
        await self.redis.rpush(key, *data)

    @staticmethod
    def _get_hash(kwargs):
        return str(hash(kwargs))
