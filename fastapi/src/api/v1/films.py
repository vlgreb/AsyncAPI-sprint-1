from http import HTTPStatus
from typing import List

from api.v1.models.api_film_models import FilmBase, FilmFull
from api.v1.models.api_query_params_model import (FilmListSearch,
                                                  SearchQueryParams)
from services.film import FilmService, get_film_service

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get('/search',
            response_model=List[FilmBase],
            summary='Поиск фильмов',
            description='Поиск по фильмам по запросу',
            response_description='Список фильмов с id, названием и рейтингом',
            tags=['Фильмы']
            )
async def film_search(film_service: FilmService = Depends(get_film_service),
                      query_params: SearchQueryParams = Depends()) -> List[FilmBase]:
    """
    Метод (ручка) для обработки запросов на поиск фильмов по запросу. Совпадения ищутся в названии и описании фильма.

    :param film_service: класс, предоставляющий интерфейс для получения информации о фильмах из БД
    :param query_params: параметры запроса API
    :return: список документов в виде Pydantic класса
    """
    films = await film_service.search_films(query=query_params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [FilmBase(**film) for film in films]


@router.get('/{film_id}',
            response_model=FilmFull,
            summary='Информация о фильме по ID',
            description='Данный endpoint предоставляет полную информацию о фильме по ID',
            response_description='ID, название, описание, жанры, рейтинг, список участников кинопроизведения',
            tags=['Фильмы']
            )
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmFull:
    """
    Метод (ручка) выводит детальную информацию по id фильма в виде Pydantic-класса FilmFull
    :param film_id: id фильма
    :param film_service: класс, предоставляющий интерфейс для получения информации о фильмах из БД
    :return:
    """
    film = await film_service.get_item(doc_id=film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return FilmFull(**film)


@router.get('',
            response_model=List[FilmBase],
            summary='Список фильмов',
            description='Список фильмов с пагинацией, фильтрацией по жанрам и сортировкой по году или рейтингу',
            response_description='Список фильмов с id, названием и рейтингом',
            tags=['Фильмы']
            )
async def film_list(film_service: FilmService = Depends(get_film_service),
                    query_params: FilmListSearch = Depends()) -> List[FilmBase]:
    """
    Метод (ручка), позволяющий получить список фильмов по различным параметрам запроса(пагинацией,
    фильтрацией по жанрам, сортировкой по рейтингу).

    :param film_service: класс, предоставляющий интерфейс для получения информации о фильмах из БД
    :param query_params: параметры запроса API
    :return:
    """
    # TODO: прокинуть параметры сортировки и реализовать
    # TODO: переделать валидацию size на дискретные значения. например, 25, 50, 100
    films = await film_service.get_list_films(query_params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [FilmBase(**film) for film in films]
