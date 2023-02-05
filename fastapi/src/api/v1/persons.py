from http import HTTPStatus
from typing import List

from api.v1.models.api_film_models import FilmBase
from api.v1.models.api_person_models import PersonBase, PersonFull
from api.v1.models.api_query_params_model import (BaseListQuery,
                                                  SearchQueryParams)
from services.person import PersonService, get_person_service

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get('/search',
            response_model=List[PersonFull],
            summary='Поиск персон',
            description='Поиск по персонам по запросу',
            response_description='Список персон с id, именем и ролью',
            tags=['Персоны']
            )
async def person_search(person_service: PersonService = Depends(get_person_service),
                        query: SearchQueryParams = Depends()) -> List[PersonBase]:
    persons = await person_service.search_persons(query=query)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')

    return [PersonFull(**person) for person in persons]


@router.get('/{person_id}/film',
            response_model=List[FilmBase],
            summary='Информация о фильмах по персоне',
            description='Данный endpoint предоставляет информацию о фильмах по персоне Id, title, imdb_rating',
            response_description='ID, полное имя, роль',
            tags=['Персоны']
            )
async def films_with_person_details(person_id: str,
                                    person_service: PersonService = Depends(get_person_service)) -> List[FilmBase]:
    films = await person_service.get_films_by_person(person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return [FilmBase(**film) for film in films]


@router.get('/{person_id}',
            response_model=PersonFull,
            summary='Информация о персоне по ID',
            description='Данный endpoint предоставляет полную информацию о персоне по ID',
            response_description='ID, полное имя, роль',
            tags=['Персоны']
            )
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> PersonFull:
    person = await person_service.get_item(doc_id=person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return PersonFull(**person)


sort_regex = "^(asc|desc)$"


@router.get('',
            response_model=List[PersonBase],
            summary='Список персон',
            description='Список персон с пагинацией',
            response_description='Список персон с id, названием и рейтингом',
            tags=['Персоны']
            )
async def person_list(person_service: PersonService = Depends(get_person_service),
                      query: BaseListQuery = Depends()) -> List[PersonBase]:
    # TODO: прокинуть параметры сортировки и реализовать
    # TODO: переделать валидацию size на дискретные значения. например, 25, 50, 100
    persons = await person_service.get_list_persons(query)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [PersonBase(**person) for person in persons]
