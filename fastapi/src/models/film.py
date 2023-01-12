from datetime import date
from typing import Optional, List
from uuid import UUID

import orjson

# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Film(BaseModel):
    id: UUID
    title: str
    description: str
    creation_date: date = None
    rating: Optional[float] = None
    genres: List[str] = ''
    actors: List[str] = ''
    directors: List[str] = ''
    writers: List[str] = ''

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps
