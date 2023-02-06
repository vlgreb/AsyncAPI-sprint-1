import asyncio

import aiohttp
import aioredis
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import connection_settings


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
async def api_session(event_loop):
    session = aiohttp.ClientSession()
    yield session
    await session.close()
