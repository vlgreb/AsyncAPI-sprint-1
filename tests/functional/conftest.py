import asyncio
import time
import uuid
from typing import List

import aiohttp
import aioredis
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from elasticsearch.helpers.errors import BulkIndexError

from tests.functional.settings import (TestSettings, connection_settings,
                                       movies_settings)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=[f'{connection_settings.es_host}:{connection_settings.es_port}'])
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    redis = await aioredis.create_redis_pool(
        (connection_settings.redis_host, connection_settings.redis_port), minsize=10, maxsize=20)
    yield redis
    redis.close()
    await redis.wait_closed()


# @pytest_asyncio.fixture
# def es_create_index(es_client):
#     async def inner(index: TestSettings):
#         print('before check index')
#         if await es_client.indices.exists(index=index.es_index):
#
#             await es_client.indices.delete(index=index.es_index)
#             print('delete index')
#
#             await es_client.indices.create(index=index.es_index,
#                                            settings=index.es_index_mapping['settings'],
#                                            mappings=index.es_index_mapping['mappings'])
#             print('create index')
#
#     return inner


async def create_index(es_client: AsyncElasticsearch, index: TestSettings):
    print('before check index')
    index_exists = await es_client.indices.exists(index=index.es_index)
    print(f'index {index.es_index} exists - ', index_exists)
    if index_exists:
        await es_client.indices.delete(index=index.es_index)
        print('delete index')

    index_exists = await es_client.indices.exists(index=index.es_index)
    print(f'index {index.es_index} exists - ', index_exists)
    print(f'create index {index.es_index}')
    await es_client.indices.create(index=index.es_index,
                                   settings=index.es_index_mapping['settings'],
                                   mappings=index.es_index_mapping['mappings'])

    index_exists = await es_client.indices.exists(index=index.es_index)
    print(f'index {index.es_index} exists - ', index_exists)


@pytest_asyncio.fixture(scope='session')
async def es_create_movies_index(es_client):
    await create_index(es_client, movies_settings)


@pytest_asyncio.fixture(scope='session')
def es_write_data(es_client):
    async def inner(data: List[dict], index: TestSettings):

        try:
            await async_bulk(es_client, data, index=index.es_index)

        except BulkIndexError:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest_asyncio.fixture(scope='function')
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


@pytest_asyncio.fixture(scope='session')
async def api_session(event_loop):
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='function')
def make_get_request(api_session):

    async def inner(query: str, query_params: dict, settings: TestSettings):
        url = f'{settings.api_prefix}{query}'
        async with api_session.get(url, params=query_params) as response:
            body = await response.json()
            status = response.status

        return {'status': status, 'length': len(body)}

    return inner
