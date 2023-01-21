import logging
from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from models.models import Film
from services.base_service import BaseService

from fastapi import Depends


class FilmService(BaseService):
    """
    Класс позволяет взаимодействовать с ElasticSearch и Redis для поиска информации по фильму, включая четкий и
    нечеткий (полнотекстовый) поиск.
    """
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis, elastic)
        self.index_name = 'movies'
        self.service_name = 'FilmService'

    async def get_film_by_id(self, doc_id: str) -> Optional[Film]:
        film = await self.get_by_id(doc_id)
        return Film(**film)

    async def get_list_films(self, page: int, size: int, genre_id: Optional[str]) -> Optional[List[Film]]:
        """
        Метод возвращает все фильмы по параметрам и фильтрации
        :param page: номер страницы
        :param size: количество фильмов на странице
        :param genre_id: ID жанра для фильтрации
        :return: list[Film]
        """

        body = {
            "from": (page - 1) * size,
            "size": size,
            "sort": [{"imdb_rating": {"order": "desc"}}]
        }

        if genre_id:
            body["query"] = {
                "nested": {
                    "path": "genres",
                    "query": {
                        "bool": {
                            "must": [{
                                "term": {
                                    "genres.id": {
                                        "value": genre_id
                                    }
                                }
                            }]
                        }
                    }
                }
            }

        return await self._get_films(body, size)

    async def _get_data_from_elastic(self, index: str, body: dict):

        try:
            data = await self.elastic.search(index=index, body=body)
            films = [Film(**item['_source']) for item in data['hits']['hits']]

            logging.info('[FilmService] get film_data from elastic')
        except NotFoundError:
            logging.info("[FilmService] can't find film_data in elastic")
            return None

        return films

    async def search_films(self, query: str, page: int, size: int) -> Optional[List[Film]]:
        """
        Полнотекстовый поиск по query
        :param query: запрос
        :param page: номер страницы
        :param size: количество фильмов на странице
        :return: list[Film]
        """
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [
                        "title^2",
                        "description"
                    ]
                }
            },
            "from": (page - 1) * size,
            "size": size
        }

        return await self._get_films(body, size)

    async def _get_films(self, body: dict, size: int) -> Optional[List[Film]]:
        """
        Метод достает данные из кэша или эластика
        :param body:
        :return:
        """
        redis_key = await self._get_hash(str(body))

        films = await self._get_list_of_data_from_cache(key=redis_key, redis_range=size)

        if not films:

            films = await self._get_data_from_elastic(index='movies', body=body)

            if not films:
                return None

            cache_data = [film.json() for film in films]

            await self._put_list_of_data_to_cache(data=cache_data, key=redis_key)

        else:
            films = [Film.parse_raw(film) for film in films]
            logging.info('[FilmService] film_data from cache')

        return films


@lru_cache()
def get_film_service(redis: Redis = Depends(get_redis),
                     elastic: AsyncElasticsearch = Depends(get_elastic), ) -> FilmService:

    return FilmService(redis, elastic)
