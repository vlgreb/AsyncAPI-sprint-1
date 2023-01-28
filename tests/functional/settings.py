import os
from pathlib import Path

from pydantic import BaseSettings, Field

from tests.functional.testdata.es_mapping import (genre_index, movies_index,
                                                  person_index)


class BaseConfig(BaseSettings):
    es_host: str = Field('http://127.0.0.1', env='ELASTIC_HOST')
    es_port: int = Field(9200, env='ELASTIC_PORT')
    redis_host: str = Field('http://127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
    service_url: str = Field('http://127.0.0.1:8001', env='SERVICE_URL')

    class Config:
        env_file = os.path.join(Path(__file__).parent.absolute(), '.env')
        env_file_encoding = 'utf-8'


class TestSettings(BaseSettings):
    es_index: str
    es_index_mapping: dict
    api_prefix: str


connection_settings = BaseConfig()

movies_settings = TestSettings(es_index='movies',
                               es_index_mapping=movies_index,
                               api_prefix=f'{connection_settings.service_url}/api/v1/films')
genre_settings = TestSettings(es_index='genres',
                              es_index_mapping=genre_index,
                              api_prefix=f'{connection_settings.service_url}/api/v1/genres')
person_settings = TestSettings(es_index='persons',
                               es_index_mapping=person_index,
                               api_prefix=f'{connection_settings.service_url}/api/v1/persons')
