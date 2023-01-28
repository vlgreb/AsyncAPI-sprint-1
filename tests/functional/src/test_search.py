import uuid

import aiohttp
import elasticsearch.helpers
import pytest

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from tests.functional.settings import movies_settings
from tests.functional.conftest import es_client, es_write_data, redis_client, es_create_index

@pytest.mark.asyncio
async def test_search():

    es_data = [{
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
    } for _ in range(60)]

    bulk_query = [
        {
            '_index': movies_settings.es_index,
            '_id': row['id'],
            '_source': row
         } for row in es_data
    ]

    # 2. Загружаем данные в ES

    # print(movies_settings.es_host)
    # print(os.getcwd())
    # print(movies_settings.es_index)
    es_client = AsyncElasticsearch(hosts=[movies_settings.es_host])
    try:
        await async_bulk(es_client, bulk_query, index=movies_settings.es_index)
    except elasticsearch.helpers.BulkIndexError:
        raise Exception('Ошибка записи данных в Elasticsearch')
    finally:
        await es_client.close()

    # 3. Запрашиваем данные из ES по API

    session = aiohttp.ClientSession()
    url = movies_settings.service_url + '/api/v1/films/search'
    query_data = {'query': 'The Star',
                  'page_number': 1,
                  'page_size': 50}
    async with session.get(url, params=query_data) as response:
        # print(response)
        body = await response.json()
        # print(body)
        headers = response.headers
        # print(headers)
        status = response.status
        # print(status)
    await session.close()

    # 4. Проверяем ответ

    assert status == 200
    assert len(body) == 50
