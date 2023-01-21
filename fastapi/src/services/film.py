import logging
from typing import Optional, List

from dataclasses import dataclass
from fastapi import Depends
from functools import lru_cache
from aioredis import Redis
from db.redis import get_redis
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from models.models import Film
from services.base_service import BaseService


@dataclass
class FilmService(BaseService):
    """
    Класс позволяет взаимодействовать с ElasticSearch и Redis для поиска информации по фильму, включая четкий и
    нечеткий (полнотекстовый) поиск.
    """
    service_name: str = 'FilmService'

    async def get_film_by_id(self, doc_id: str) -> Optional[Film]:
        film = await self.get_by_id(doc_id)
        return Film(**film)

    async def get_films(self, page: int, size: int, genre_id: Optional[str]) -> Optional[List[Film]]:
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

        redis_key = await self._get_hash(str(body))

        films = await self._get_list_of_data_from_cache(key=redis_key, redis_range=size)

        if not films:

            films = await self._get_data_from_elastic(index='movies', body=body)

            if not films:
                return None

            cache_data = [film.json() for film in films]

            logging.info(films)

            await self._put_list_of_data_to_cache(data=cache_data, key=redis_key)

        else:
            films = [Film.parse_raw(film) for film in films]
            logging.info('[FilmService] film_data from cache')

        return films

    async def _get_data_from_elastic(self, index: str, body: dict):

        try:
            data = await self.elastic.search(index=index, body=body)
            films = [Film(**item['_source']) for item in data['hits']['hits']]

            logging.info('[FilmService] get film_data from elastic')
        except NotFoundError:
            logging.info("[FilmService] can't find film_data in elastic")
            return None

        return films


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic, index_name='movies')
