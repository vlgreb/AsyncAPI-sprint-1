import logging
from functools import lru_cache
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

        try:

            body = {
                "from": (page - 1) * size,
                "size": size,
                "sort": [{"imdb_rating": {"order": "desc"}}]
            }

            data = await self.elastic.search(index='movies', body=body)

            results = data['hits']['hits']

            logging.info('[FilmService] from elastic')

        except NotFoundError:
            logging.info("[FilmService] can't find in elastic")
            return None

        films = [Film(**item['_source']) for item in results]
        logging.info(f"[FilmService] {films}")
        return films


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
