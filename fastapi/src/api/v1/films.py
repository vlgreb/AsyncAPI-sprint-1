import logging
from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from services.film import FilmService, get_film_service

router = APIRouter()


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]


@router.get('/{film_id}',
            response_model=Film,
            summary='Информация о фильме по ID',
            description='Данный endpoint предоставляет полную информацию о фильме по ID',
            response_description='ID, название, описание, жанры, рейтинг, список участников кинопроизведения',
            tags=['Фильмы']
            )
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return Film(id=film.id, title=film.title)


sort_regex = "^(asc|desc)$"


@router.get('',
            response_model=List[Film],
            summary='Список фильмов',
            description='Список фильмов с пагинацией, фильтрацией по жанрам и сортировкой по году или рейтингу',
            response_description='Список фильмов с id, названием и рейтингом',
            tags=['Фильмы']
            )
async def film_list(film_service: FilmService = Depends(get_film_service),
                    page: int = Query(default=1, alias="page_number", ge=1),
                    size: int = Query(default=25, alias="page_size", ge=1, le=100),
                    sort_imdb: Optional[str] = Query(default=None, regex=sort_regex, alias='sort_by_rating'),
                    sort_year: Optional[str] = Query(default=None, regex=sort_regex, alias='sort_by_year')
                    ):
    films = await film_service.get_films(page=page, size=size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [Film(id=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]
