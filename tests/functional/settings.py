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


class MoviesSettings(BaseConfig):

    es_index: str = Field('movies_test')
    es_index_mapping: dict = movies_index


class GenreSettings(BaseConfig):

    es_index: str = Field('genres_test')
    es_index_mapping: dict = genre_index


class PersonSettings(BaseConfig):

    es_index: str = Field('persons_test')
    es_index_mapping: dict = person_index


connection_settings = BaseConfig()

movies_settings = MoviesSettings()

# print(connection_settings.dict())
# print(os.path.join(os.getcwd(), '.env'))