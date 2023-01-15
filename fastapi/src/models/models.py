from datetime import date
from typing import Optional, List
from uuid import UUID

import orjson

# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class IdMixin(BaseModel):
    id: UUID

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(IdMixin):
    full_name: str
    role: str
    film_ids: List[UUID]


class Genre(IdMixin):
    name: str


class Film(IdMixin):
    title: str
    description: str
    creation_date: date = None
    rating: Optional[float] = None
    genres: List[Genre]
    actors: List[Person]
    directors: List[Person]
    writers: List[Person]


if __name__ == '__main__':
    film = Film.parse_file('film_test.json')
    print(film)
