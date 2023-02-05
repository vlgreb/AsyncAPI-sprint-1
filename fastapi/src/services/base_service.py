import logging
from abc import ABC, abstractmethod
from typing import List

from aioredis import Redis
from db.db_data_getter import ElasticDataGetter
from db.storage import RedisStorage
from utils.cache import cache


class DataService(ABC):
    """Абстрактный класс для работы с данными"""

    @abstractmethod
    async def get_item(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_list_of_items(self, *args, **kwargs):
        pass


class BaseDataService(DataService):
    """Класс для взаимодействия с БД и кэшем"""

    def __init__(self, elastic_client, redis_client: Redis):
        self._cache = RedisStorage(redis_client)
        self._db_handler = ElasticDataGetter(elastic_client)
        self.index_name = ''

    @cache
    async def get_item(self, doc_id: str) -> dict | None:
        """
        Метод получает документ в виде словаря

        :param doc_id: id документа в индексе БД
        :return: документ в виде словаря
        """

        return await self._db_handler.get_by_id(index=self.index_name, doc_id=doc_id)

    @cache
    async def get_list_of_items(self, api_query_params: dict, elastic_query: dict,
                                index_name: str = None) -> List[dict] | None:
        """
        Метод получает список документов в виде словарей
        :param api_query_params:
        :param elastic_query:
        :param index_name:
        :return:
        """
        index_name = index_name if index_name else self.index_name
        return await self._db_handler.get_by_query(index=index_name, query=elastic_query)

    def _get_key(self, *args, **kwargs) -> str | None:
        """
        Метод формирует ключ для постоянного хранилища на основе имени индекса ElasticSearch и параметров
        запроса ручек.
        :param query_params: параметры запроса
        :return:
        """

        if args:
            param = args[0]
        else:
            param = kwargs.get('doc_id') or kwargs.get('api_query_params')

        if not param:
            raise AttributeError("Check naming to generate cache key")

        return f'{self.index_name}::{param}'

    async def _validation_page(self, page: int, size: int, body: dict) -> int:

        try:
            docs_in_db = await self._db_handler.get_count_docs(index=self.index_name, body=body)

            new_page = docs_in_db // size + bool(docs_in_db % size)
            if docs_in_db and page > new_page:
                page = new_page

        except (KeyError, TypeError):
            logging.info("[%s] can't count docs in db", type(self).__name__)

        return page
