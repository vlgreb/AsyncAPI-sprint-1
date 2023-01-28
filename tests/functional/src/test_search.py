import logging
import time
from typing import List

import pytest

from tests.functional.conftest import (es_client, es_movies_data,
                                       es_write_data, redis_client)
from tests.functional.settings import movies_settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': 'The Star',
             'page_number': 1,
             'page_size': 50},
            {'status': 200, 'length': 50}
        ),
        (
            {'query': 'Mashed potato',
             'page_number': 1,
             'page_size': 50},
            {'status': 404, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_movies_search(make_get_request, es_write_data, es_movies_data: List[dict],
                             query_data: dict, expected_answer: dict):
    await es_write_data(es_movies_data, movies_settings)
    response = await make_get_request('/search', query_data, movies_settings)
    # time.sleep(0.1)
    assert expected_answer == response
