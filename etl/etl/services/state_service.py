import abc
from json.decoder import JSONDecodeError
from typing import Any

from redis import Redis


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние из постоянного хранилища"""
        pass


class RedisStorage(BaseStorage):
    def __init__(self, redis_adapter: Redis):
        self.redis_adapter = redis_adapter

    def save_state(self, state: dict) -> None:
        self.redis_adapter.mset(state)

    def retrieve_state(self) -> dict:
        """Загрузить состояние из постоянного хранилища"""
        result = {key.decode("utf-8"): self.redis_adapter[key].decode("utf-8")
                  for key in self.redis_adapter.scan_iter()}
        return result

    def _clear_cache(self):
        """Очистить кэш"""
        self.redis_adapter.flushdb()


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        json_dict = self.storage.retrieve_state()
        json_dict[key] = value
        self.storage.save_state(json_dict)

    def get_state(self, key: str, default=None) -> Any:
        """Получить состояние по определённому ключу"""
        json_dict = self.storage.retrieve_state()
        try:
            return json_dict[key]
        except (JSONDecodeError, KeyError):
            return default


if __name__ == '__main__':
    print("State is running")
