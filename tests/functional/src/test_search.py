import uuid

import aiohttp
import elasticsearch.helpers
import pytest
from typing import List
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from tests.functional.settings import movies_settings
from tests.functional.conftest import (es_client, es_write_data, redis_client, es_movies_data)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': 'The Star',
             'page_number': 1,
             'page_size': 50},
            {'status': 200, 'length': 0}
        ),
        (
            {'query': 'Mashed potato',
             'page_number': 1,
             'page_size': 50},
            {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_movies_search(make_get_request, es_write_data, es_movies_data: List[dict], query_data: dict, expected_answer: dict):
    await es_write_data(es_movies_data, movies_settings)
    response = await make_get_request('/search', query_data, movies_settings)

    assert expected_answer == response
