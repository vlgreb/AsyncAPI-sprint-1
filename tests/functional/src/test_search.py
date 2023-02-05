import pytest

from tests.functional.settings import movies_settings, person_settings
from tests.functional.testdata.search_data import (
    FILM_FULL_TEXT_SEARCH, FILMS_SEARCH_STATUS_AND_LENGTH_QUERIES,
    PERSONS_FUZZY_SEARCH_QUERIES)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    FILMS_SEARCH_STATUS_AND_LENGTH_QUERIES
)
@pytest.mark.asyncio
async def test_movies_search(get_data, query_data: dict, expected_answer: dict):
    """Тест на нечеткий поиск фильмов и статус ответа. Также тестируется отсутствие результата."""

    response = await get_data('/search', query_data, movies_settings)
    assert expected_answer == response.validation


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PERSONS_FUZZY_SEARCH_QUERIES
)
@pytest.mark.asyncio
async def test_person_fuzzy_search(get_data, query_data: dict, expected_answer: dict):
    """Тест на нечеткий поиск персоны."""

    response = await get_data('/search', query_data, person_settings)
    assert expected_answer == response.data


@pytest.mark.parametrize(
    'query_data, expected_answer',
    FILM_FULL_TEXT_SEARCH
)
@pytest.mark.asyncio
async def test_films_fuzzy_search(get_data, query_data: dict, expected_answer: dict):
    """Тест на нечеткий поиск фильмов."""

    response = await get_data('/search', query_data, movies_settings)
    assert expected_answer == response.data
