from dataclasses import asdict
from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from api.v1.models.api_query_params_model import BaseListQuery
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from services.base_service import BaseDataService

from fastapi import Depends


class GenreService(BaseDataService):
    """
    Класс позволяет взаимодействовать с ElasticSearch и Redis для поиска информации по жанру, включая четкий и
    нечеткий (полнотекстовый) поиск.
    """
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(elastic, redis)
        self.index_name = 'genres'

    async def get_list_genres(self, query: BaseListQuery) -> Optional[List[dict]]:
        """
        Метод возвращает все жанры
        :param query: количество жанров на странице
        :return: list[Genre]
        """

        query.page = await self._validation_page(query.page, query.size, dict())

        body = {
            "from": (query.page - 1) * query.size,
            "size": query.size,
            "sort": [{
              "name.raw": {
                "order": "asc"
              }
            }]
        }

        return await self.get_list_of_items(api_query_params=asdict(query), elastic_query=body)


@lru_cache()
def get_genre_service(redis: Redis = Depends(get_redis),
                      elastic: AsyncElasticsearch = Depends(get_elastic), ) -> GenreService:

    return GenreService(redis, elastic)
