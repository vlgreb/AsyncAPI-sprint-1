from dataclasses import dataclass
from typing import Optional

from fastapi import Query

sort_regex = "^(asc|desc)$"


@dataclass
class BaseListQuery:
    page: int = Query(default=1, alias="page_number", ge=1)
    size: int = Query(default=25, alias="page_size", ge=1, le=100)


@dataclass
class FilmListSearch(BaseListQuery):
    sort_imdb: Optional[str] = Query(default='desc', regex=sort_regex, alias='sort_by_rating')
    genre_id: Optional[str] = Query(default=None, alias='filter[genre]')


@dataclass
class SearchQueryParams(BaseListQuery):
    query: Optional[str] = Query(..., alias='query')
