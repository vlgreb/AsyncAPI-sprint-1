from dataclasses import asdict
from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from api.v1.models.api_query_params_model import (BaseListQuery,
                                                  SearchQueryParams)
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from services.base_service import BaseDataService

from fastapi import Depends


class PersonService(BaseDataService):
    """
    Класс позволяет взаимодействовать с ElasticSearch и Redis для поиска информации по персоне, включая четкий и
    нечеткий (полнотекстовый) поиск.
    """

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(elastic, redis)
        self.index_name = 'persons'

    async def get_list_persons(self, query: BaseListQuery) -> Optional[List[dict]]:
        """
        Метод возвращает все персоны по параметрам и фильтрации
        :param query: номер страницы
        :return: list[Person]
        """

        query.page = await self._validation_page(query.page, query.size, dict())

        body = {
            "from": (query.page - 1) * query.size,
            "size": query.size,
            "sort": [{
              "full_name.raw": {
                "order": "desc"
              }
            }]
        }

        return await self.get_list_of_items(api_query_params=asdict(query), elastic_query=body)

    async def search_persons(self, query: SearchQueryParams) -> Optional[List[dict]]:
        """
        Полнотекстовый поиск по query
        :param query: запрос
        :return: list[Person]
        """
        body = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "full_name": {
                                    "query": query.query,
                                    "fuzziness": "AUTO"
                                }
                            }
                        },
                        {
                            "fuzzy": {
                                "full_name": {"value": query.query}
                            }
                        }
                    ]
                }
            }
        }

        query.page = await self._validation_page(query.page, query.size, body)

        body["from"] = (query.page - 1) * query.size
        body["size"] = query.size

        return await self.get_list_of_items(api_query_params=asdict(query), elastic_query=body)

    async def get_films_by_person(self, person_id: str) -> Optional[List[dict]]:

        # TODO: прикрутить пагинацию

        multi_field_query = [{
            "nested": {
                "path": role,
                "query": {
                    "bool": {
                        "must": [{
                            "term": {
                                f"{role}.id": {
                                    "value": person_id
                                }
                            }
                        }]
                    }
                }
            }
        } for role in ('actors', 'writers', 'directors')]

        body = {
            "query": {
                "bool": {
                    "should": multi_field_query
                }
            },
            "sort": [{"imdb_rating": {"order": "desc"}}]
        }

        return await self.get_list_of_items(api_query_params={'query': f'/{person_id}/film'},
                                            elastic_query=body, index_name='movies')


@lru_cache()
def get_person_service(redis: Redis = Depends(get_redis),
                       elastic: AsyncElasticsearch = Depends(get_elastic), ) -> PersonService:
    return PersonService(redis, elastic)
