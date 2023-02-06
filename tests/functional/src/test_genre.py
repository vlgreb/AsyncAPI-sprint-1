import pytest
from aioredis import Redis
from orjson import orjson

from tests.functional.utils.helpers import get_data
from tests.functional.settings import genre_settings
from tests.functional.testdata.genre_data import (ADVENTURE_GENRE,
                                                  FIRST_PAGE_GENRES,
                                                  LAST_PAGE_GENRES)


@pytest.mark.parametrize(
    'query, expected_answer',
    [
        (
          "/None",
          {"detail": "genre not found"}
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_genre_by_id(api_session, query, expected_answer):
    """
    Тест на запрос несуществующего жанра
    :param query:
    :param expected_answer:
    :return: GenreFull.as_dict
    """
    response = await get_data(api_session=api_session, query=query, query_params=None, settings=genre_settings)

    assert expected_answer == response.data


@pytest.mark.parametrize(
    'query_params, expected_answer',
    [
        (
            {
                "page_number": 1,
                "page_size": 10
            }
            , FIRST_PAGE_GENRES
        ),
        (
            {
                "page_number": 4,
                "page_size": 10
            }
            , LAST_PAGE_GENRES
        ),
        (
            {
                "page_number": 1000,
                "page_size": 10
            }
            , LAST_PAGE_GENRES
        )
    ]
)
@pytest.mark.asyncio
async def test_get_film_by_genre(api_session, query_params, expected_answer):
    """
    Тесты списка жанров + валидация последней страницы
    :param query_params:
    :param expected_answer:
    :return: GenreFull.as_dict
    """

    response = await get_data(api_session=api_session, query='', query_params=query_params, settings=genre_settings)

    assert expected_answer == response.data


@pytest.mark.parametrize(
    'query, expected_answer',
    [
        (
            '/120a21cf-9097-479e-904a-13dd7198c1dd',
            ADVENTURE_GENRE
        ),
    ]
)
@pytest.mark.asyncio
async def test_cache_genre(api_session, redis_client: Redis, query: str, expected_answer):
    """Тест на поиск жанра по ID + на работу кэша"""

    key = f'genres::{query.strip("/")}'

    await redis_client.delete(key)

    assert await redis_client.exists(key) == 0

    response = await get_data(api_session=api_session, query=query, query_params=None, settings=genre_settings)

    assert await redis_client.exists(key)

    data_from_cache = await redis_client.get(key)

    assert expected_answer == response.data == orjson.loads(data_from_cache)
