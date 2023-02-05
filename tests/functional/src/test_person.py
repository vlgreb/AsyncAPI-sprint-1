import orjson
import pytest
from aioredis import Redis

from tests.functional.settings import person_settings
from tests.functional.testdata.person_data import (FILMS_WITH_PERSON_PARAMS,
                                                   LAST_PAGE_PERSONS,
                                                   PERSON_BY_ID_PARAMS,
                                                   PERSONS_LIST_REQUEST_STATUS,
                                                   PERSONS_PAGINATION_PARAMS,
                                                   TEST_PERSON_CACHE)


@pytest.mark.parametrize(
    'query, expected_answer',
    PERSONS_LIST_REQUEST_STATUS
)
@pytest.mark.asyncio
async def test_get_persons_list_request_status(get_data, query, expected_answer):
    """Тест на статус и длину возвращаемого объекта по запросу."""

    response = await get_data(query=query, query_params=None, settings=person_settings)

    assert expected_answer == response.validation


@pytest.mark.parametrize(
    'query, expected_answer',
    PERSON_BY_ID_PARAMS
)
@pytest.mark.asyncio
async def test_get_person_by_id(get_data, query, expected_answer):
    """Тест на корректность возврата данных персоны по ID + запрос несуществующего человека."""
    response = await get_data(query=query, query_params=None, settings=person_settings)

    assert expected_answer == response.data


@pytest.mark.parametrize(
    'query_params, expected_answer',
    PERSONS_PAGINATION_PARAMS
)
@pytest.mark.asyncio
async def test_persons_pagination(get_data, query_params, expected_answer):
    """Тест проверяет пагинацию."""
    response = await get_data(query='', query_params=query_params, settings=person_settings)

    assert expected_answer == response.validation


@pytest.mark.asyncio
async def test_max_page_size(get_data):
    """
    Тест проверяет пагинацию при получении таких параметров page_number и page_size со значением,
    превышающим максимальное
    количество фильмов. API должен возвращать последнюю страницу хотя бы с одним элементом.
    """

    query_params = {'page_number': 1000000, 'page_size': 25}

    response = await get_data(query='', query_params=query_params, settings=person_settings)

    assert response.validation['status'] == 200 and 1 <= response.validation['length'] <= 25


@pytest.mark.parametrize(
    'query, expected_answer',
    FILMS_WITH_PERSON_PARAMS
)
@pytest.mark.asyncio
async def test_films_by_person_id(get_data, query, expected_answer):
    """Тест на получение списка фильмов, в которых принимал участие человек по его ID."""

    response = await get_data(query=query, query_params=None, settings=person_settings)

    assert expected_answer == response.data


# TODO: тесты ниже

@pytest.mark.parametrize(
    'query, expected_answer',
    TEST_PERSON_CACHE
)
@pytest.mark.asyncio
async def test_cache_person(get_data, redis_client: Redis, query: str, expected_answer):
    """Тест на получение списка фильмов по ID персоны"""

    key = f'persons::{query.strip("/")}'

    await redis_client.delete(key)

    assert await redis_client.exists(key) == 0

    response = await get_data(query=query, query_params=None, settings=person_settings)

    assert await redis_client.exists(key)

    data_from_cache = await redis_client.get(key)

    assert expected_answer == response.data == orjson.loads(data_from_cache)


@pytest.mark.parametrize(
    'query_params, expected_answer',
    [
        (
            {
                "page_number": 168,
                "page_size": 25
            }
            , LAST_PAGE_PERSONS
        ),
        (
            {
                "page_number": 9000,
                "page_size": 25
            }
            , LAST_PAGE_PERSONS
        )
    ]
)
@pytest.mark.asyncio
async def test_get_film_by_genre(get_data, query_params, expected_answer):
    """
    Тесты валидации последней страницы
    :param query_params:
    :param expected_answer:
    :return: GenreFull.as_dict
    """

    response = await get_data(query='', query_params=query_params, settings=person_settings)

    assert expected_answer == response.data
