from pydantic import BaseModel


class ResponseFromApi(BaseModel):
    """Модель для валидации ответов сервиса fastapi"""
    data: list | dict
    validation: dict


class BaseListQuery(BaseModel):
    page: int
    size: int
