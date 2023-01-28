import pytest
import aioredis
import uuid

import aiohttp
from typing import List

from elasticsearch.helpers.errors import BulkIndexError
from elasticsearch.helpers import async_bulk
from elasticsearch import AsyncElasticsearch, Elasticsearch
from tests.functional.settings import TestSettings, connection_settings, movies_settings, genre_settings, person_settings


@pytest.fixture(scope='session')
async def es_client():
    es_client = AsyncElasticsearch(hosts=[connection_settings.es_host])
    yield es_client
    await es_client.close()


@pytest.fixture(scope='session')
async def redis_client():
    redis_client = await aioredis.create_redis_pool(
        (connection_settings.redis_host, connection_settings.redis_port), minsize=10, maxsize=20)
    yield redis_client
    redis_client.close()
    await redis_client.wait_closed()


# @pytest.fixture
# async def es_create_index(es_client: AsyncElasticsearch, index: TestSettings):
#     yield await es_client.indices.create(index=index.es_index, **index.es_index_mapping)
#     await es_client.indices.delete(index=index.es_index)


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: List[dict], index: TestSettings):
        try:
            await async_bulk(es_client, data, index=index.es_index)
        except BulkIndexError:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def es_movies_data() -> List[dict]:
    data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genres': [
            {'id': 'genre1', 'name': 'Action'},
            {'id': 'genre2', 'name': 'Sci-Fi'}
        ],
        'creation_date': 2022,
        'title': 'The Star',
        'description': 'New World',
        'actors': [
            {'id': '111', 'full_name': 'Ann'},
            {'id': '222', 'full_name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'full_name': 'Ben'},
            {'id': '444', 'full_name': 'Howard'}
        ],
        'directors': [
            {'id': '555', 'full_name': 'Igor'},
            {'id': '777', 'full_name': 'Vladimir'}
        ]
    } for _ in range(110)]

    return [
        {
            '_index': movies_settings.es_index,
            '_id': row['id'],
            '_source': row
        } for row in data
    ]


@pytest.fixture(scope='session')
def api_session():
    session = aiohttp.ClientSession()
    yield session
    session.close()


@pytest.fixture()
def make_get_request():
    async def inner(query: str, query_params: dict, settings: TestSettings):
        session = aiohttp.ClientSession()
        url = connection_settings.service_url + settings.api_prefix + query
        async with api_session.get(url, params=query_params) as response:
            body = await response.json()
            status = response.status

        await session.close()
        return {'status': status, 'length': len(body)}
    return inner
