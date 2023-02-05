from http import HTTPStatus
from typing import List

from api.v1.models.api_genre_models import GenreBase
from api.v1.models.api_query_params_model import BaseListQuery
from services.genre import GenreService, get_genre_service

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


sort_regex = "^(asc|desc)$"


@router.get('/{genre_id}',
            response_model=GenreBase,
            summary='Информация о жанре',
            description='Данный endpoint предоставляет информацию о жанре',
            response_description='ID, название жанра',
            tags=['Жанры']
            )
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> GenreBase:
    genre = await genre_service.get_item(doc_id=genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return GenreBase(**genre)


@router.get('',
            response_model=List[GenreBase],
            summary='Список жанров',
            description='Список жанров с пагинацией',
            response_description='Список жанров с id и названием',
            tags=['Жанры']
            )
async def genre_list(genre_service: GenreService = Depends(get_genre_service),
                     query: BaseListQuery = Depends()) -> List[GenreBase]:
    # TODO: прокинуть параметры сортировки и реализовать
    # TODO: переделать валидацию size на дискретные значения. например, 25, 50, 100
    genres = await genre_service.get_list_genres(query)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')

    return [GenreBase(**genre) for genre in genres]
