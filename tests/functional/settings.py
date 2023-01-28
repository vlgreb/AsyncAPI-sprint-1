import os

from pydantic import BaseSettings, Field

from tests.functional.testdata.es_mapping import person_index, genre_index, movies_index

from pathlib import Path


class BaseConfig(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    redis_host: str = Field('http://127.0.0.1:6379', env='REDIS_HOST')
    service_url: str = Field('http://127.0.0.1:8001', env='SERVICE_URL')

    class Config:
        env_file = os.path.join(Path(__file__).parent.absolute(), '.env')
        env_file_encoding = 'utf-8'


class TestSettings(BaseSettings):
    es_index: str
    es_index_mapping: dict
    api_prefix: str


connection_settings = BaseConfig()

movies_settings = TestSettings(es_index='movies_test',
                               es_index_mapping=movies_index,
                               api_prefix='/api/v1/films')
genre_settings = TestSettings(es_index='genres_test',
                              es_index_mapping=genre_index,
                              api_prefix='/api/v1/genres')
person_settings = TestSettings(es_index='persons_test',
                               es_index_mapping=person_index,
                               api_prefix='/api/v1/persons')


print(movies_settings.dict())