import abc
from json import JSONDecodeError
from typing import Any, Dict

import redis
import redis.exceptions as redis_e
from conn_data import redis_data
from my_backoff import backoff


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния.

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, key: str, value: Any) -> None:
        """Сохранить состояние в хранилище."""

    @abc.abstractmethod
    def retrieve_state(self, key: str) -> Dict[str, Any]:
        """Получить состояние из хранилища."""


class RedisStorage(BaseStorage):
    def __init__(self, redis_data: dict) -> None:
        self.redis_data = redis_data
        self.connection: redis.StrictRedis = self.get_redis_connection()

    @backoff(
        errors=(
            redis_e.ConnectionError,
            redis_e.TimeoutError,
            redis_e.ResponseError,
        ),
        client_errors=(
            redis_e.AuthenticationError,
            redis_e.NoScriptError,
            redis_e.ReadOnlyError,
            redis_e.InvalidResponse,
        ),
    )
    def get_redis_connection(self) -> redis.StrictRedis:
        """Создание соединения ES"""
        return redis.StrictRedis(
            unix_socket_path=self.redis_data["unix_socket_path"], db=1
        )

    def save_state(self, key: str, value: Any) -> None:
        """Сохранить состояние в хранилище."""
        self.connection.set(key, value.encode())

    def retrieve_state(self, key: str) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        data = self.connection.get(key)
        return data.decode() if data else None


class State:
    """Класс для работы с состояниями."""

    def __init__(
        self,
        storage: BaseStorage = None,
    ) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        self.storage.save_state(key=key, value=value)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        try:
            result = self.storage.retrieve_state(key=key)
            return None if result == "None" else result
        except JSONDecodeError as e:
            raise JSONDecodeError(f"{e}")


storage = RedisStorage(redis_data)
state = State(storage=storage)
