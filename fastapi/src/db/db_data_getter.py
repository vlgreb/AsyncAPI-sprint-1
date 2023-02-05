from abc import ABC, abstractmethod
from typing import List

from elasticsearch import AsyncElasticsearch, NotFoundError


class DBDataGetter(ABC):

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        """
        Метод предназначен для получения данных по определенному ключу/id из базы данных.
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    async def get_by_query(self, *args, **kwargs):
        """
        Метод для получения одного или множества данных из БД по определенному запросу.
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    async def get_count_docs(self, *args, **kwargs):
        """
        Метод для получения количества документов в БД
        :param args:
        :param kwargs:
        :return:
        """
        pass


class ElasticDataGetter(DBDataGetter):
    def __init__(self, elastic_client: AsyncElasticsearch):
        self.elastic_client = elastic_client

    async def get_by_id(self, index: str, doc_id: str) -> dict | None:
        """
        Метод позволяет получить документ из индекса ElasticSearch
        :param index: название индекса ElasticSearch
        :param doc_id: id документа в индексе
        :return: документ из индекса в виде словаря
        """
        try:
            doc = await self.elastic_client.get(index=index, id=doc_id)
            return doc['_source']

        except NotFoundError:
            return None

    async def get_by_query(self, index: str, query: dict) -> List[dict] | None:
        """
        Метод позволяет найти документы по запросу к ElasticSearch
        :param index: название индекса ElasticSearch
        :param query: запрос к ElasticSearch в виде словаря
        :return: список документов в виде словарей или None
        """
        try:
            data = await self.elastic_client.search(index=index, body=query)
            return [item['_source'] for item in data['hits']['hits']]

        except NotFoundError:
            return None

    async def get_count_docs(self, index: str, body: dict) -> int | None:
        """
        Метод для получения количества документов в Elastic
        :param index: название индекса ElasticSearch
        :param body: запрос к ElasticSearch в виде словаря
        :return: список документов в виде словарей или None
        """
        try:
            data = await self.elastic_client.count(index=index, body=body)
            return data.get("count")

        except NotFoundError:
            return None
