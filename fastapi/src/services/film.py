import json
import logging
from functools import lru_cache
from hashlib import md5
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.models import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id, doc_type='_doc')
            logging.info('[FilmService] from elastic by id')
        except NotFoundError:
            logging.info("[FilmService] can't find in elastic by id")
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        logging.info('[FilmService] from cache by id')
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        logging.info('[FilmService] write to cache by id')
        await self.redis.set(film.id, film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def get_films(self, page: int, size: int):

        body = {
            "from": (page - 1) * size,
            "size": size,
            "sort": [{"imdb_rating": {"order": "desc"}}]
        }

        redis_key = await self._get_hash(str(body))

        films = await self._get_data_from_cache(key=redis_key, redis_range=size)

        if not films:

            films = await self._get_data_from_elastic(index='movies', body=body)

            if not films:
                return None

            cache_data = [film.json() for film in films]

            logging.info(films)

            await self._put_data_to_cache(data=cache_data, key=redis_key)

        else:
            films = [Film.parse_raw(film) for film in films]
            logging.info('[FilmService] film_data from cache')

        return films

    @staticmethod
    async def _get_hash(kwargs):
        return str(hash(kwargs))

    async def _get_data_from_cache(self, key: str, redis_range: int):

        data = await self.redis.lrange(key, 0, redis_range)

        return data

    async def _put_data_to_cache(self, data: list, key: str):

        logging.info('[FilmService] write film_data to cache')
        await self.redis.rpush(key, *data)

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
    return FilmService(redis, elastic)
