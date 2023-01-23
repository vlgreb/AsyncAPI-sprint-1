import logging
from typing import Optional, List

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from api.v1.models.api_film_models import FilmFull
from api.v1.models.api_person_models import PersonFull
from api.v1.models.api_genre_models import Genre
from models.models import Film, Person

MODELS = {
    "Film": Film,
    "Person": Person
}

CACHE_EXPIRE_IN_SECONDS = 60 * 5


class BaseDataService:
    """
    Класс представляет базовый интерфейс для работы с ElasticSearch и Redis. Получение по id (или прочему ключу)
    документов и их кеширование.
    """
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index_name: str = '', service_name: str = 'base'):
        self.redis = redis
        self.elastic = elastic
        self.index_name = index_name
        # TODO: выпилить переменную service_name, если получится
        self.service_name = service_name
        self.model = None

    async def get_by_id(self, doc_id: str) -> FilmFull | PersonFull | Genre | None:
        """
        Возвращает документ по ключу (id). Ищет документ по ключу doc_id в кэше Redis и,
        если не находит, обращается к ElasticSearch. Возвращает None при отсутствии в Elastic.

        :param doc_id: строка (ключ, id), по которой ищется документ
        :return: экземпляр модели данных self.model (FilmFull | PersonFull | Genre) или None
        """
        data = await self._get_item_from_cache(doc_id)
        if not data:
            data = await self._get_item_from_elastic(doc_id)
            if not data:
                return None
            await self._put_item_to_cache(data)

        else:
            data = self.model.parse_raw(data)
        return data

    async def _get_item_from_cache(self, doc_id: str) -> FilmFull | PersonFull | Genre | None:
        """
        Ищет документ по ключу doc_id в кэше Redis
        :param doc_id: строка (ключ, id), по которой ищется документ
        :return: FilmFull | PersonFull | Genre | None
        """
        if self.redis.exists(doc_id):
            logging.info(f'[{self.service_name}] from cache by id')
            return await self.redis.get(doc_id)

    async def _put_item_to_cache(self, doc: FilmFull | PersonFull | Genre) -> None:
        """
        Сохраняет документ в кэш Redis.
        :param doc: экземпляр модели данных FilmFull | PersonFull | Genre
        :return: None
        """
        logging.info(f'[{self.service_name}] write to cache by id')
        await self.redis.set(doc.id, doc.json(), expire=CACHE_EXPIRE_IN_SECONDS)

    async def _get_item_from_elastic(self, doc_id: str) -> FilmFull | PersonFull | Genre | None:
        """

        :param doc_id: строка (ключ, id), по которой ищется документ
        :return: FilmFull | PersonFull | Genre | None
        """
        try:
            doc = await self.elastic.get(index=self.index_name, id=doc_id)
            logging.info(f'[{self.service_name}] from elastic by id')

            result = self.model(**doc['_source'])
        except NotFoundError:
            logging.info(f'[{self.service_name}] can\'t find in elastic by id')
            return None
        return result

    async def _get_full_data_from_cache(self, key: str, redis_range: int) -> Optional[list]:
        """
        Метод предназначен для получения массива (списка) данных из кэша
        :param key: ключ, по которому требуеся достать данные из кэша
        :param redis_range:
        :return: Optional[list]
        """
        data = await self.redis.lrange(key, 0, redis_range)
        return data

    async def _put_full_data_to_cache(self, data: list, key: str):
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

    async def _get_data(self, body: dict, size: int, index_name: str = None,
                        model: str = None) -> List[FilmFull | PersonFull | Genre] | None:
        """
        Метод достает данные из кэша или эластика
        :param body: тело запроса
        :param size: количество записей
        :param index_name: имя индекса
        :param model: модель для парсинга возвращаемого результата
        :return:
        """

        if not model:
            model_class = self.model
        else:
            model_class = MODELS[model]

        if not index_name:
            index_name = self.index_name

        redis_key = self._get_hash(str(body))

        data = await self._get_full_data_from_cache(key=redis_key, redis_range=size)

        if not data:

            data = await self._get_data_from_elastic(body=body, index=index_name, model=model)

            if not data:
                return None

            cache_data = [item.json() for item in data]

            await self._put_full_data_to_cache(data=cache_data, key=redis_key)

        else:
            data = [model_class.parse_raw(item) for item in data]
            logging.info(f'[{self.service_name}] data from cache')

        return data

    async def _get_data_from_elastic(self, body: dict, index: str,
                                     model: str) -> List[FilmFull | PersonFull | Genre] | None:
        """
        Возвращает список данных из кэша или Elastic
        :param body: тело запроса к elasticsearch
        :return: List[FilmFull | PersonFull | Genre] | None
        """

        if not model:
            model_class = self.model
        else:
            model_class = MODELS[model]

        try:
            data = await self.elastic.search(index=index, body=body)
            data = [model_class(**item['_source']) for item in data['hits']['hits']]

            logging.info(f'[{self.service_name}] get data from elastic')
        except NotFoundError:
            logging.info(f"[{self.service_name}] can't find data in elastic")
            return None

        return data
