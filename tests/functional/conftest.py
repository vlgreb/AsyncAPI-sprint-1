import pytest
import aioredis

from typing import List

from elasticsearch.helpers.errors import BulkIndexError
from elasticsearch.helpers import async_bulk
from elasticsearch import AsyncElasticsearch
from tests.functional.settings import connection_settings


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


@pytest.fixture
def es_create_index(es_client: AsyncElasticsearch):
    async def inner(data: List[dict], ):
        try:
            await async_bulk(es_client, bulk_query, index=movies_settings.es_index)
        except BulkIndexError:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: List[dict], ):
        try:
            await async_bulk(es_client, bulk_query, index=movies_settings.es_index)
        except BulkIndexError:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner
