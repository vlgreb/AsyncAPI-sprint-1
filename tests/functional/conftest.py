import asyncio
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

from .testdata.data_generator import get_movies_list


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


@pytest_asyncio.fixture(scope='session')
async def es_create_movies_index(es_client):
    await create_index(es_client, movies_settings)


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
def es_write_data(es_client):
    async def inner(data: List[dict], index: TestSettings):

        try:
            await async_bulk(es_client, data, index=index.es_index)

        except BulkIndexError:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner




MOVIES_COUNT = 110

@pytest_asyncio.fixture(scope='session')
def es_movies_data() -> List[dict]:
    return get_movies_list(MOVIES_COUNT)


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
