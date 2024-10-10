import abc
from typing import Any

import redis
import redis.exceptions as redis_e
from core.config import RedisData
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
    def retrieve_state(self, key: str) -> str | None:
        """Получить состояние из хранилища."""

    @abc.abstractmethod
    def delete_state(self, key: str) -> None:
        """Удалить состояние из хранилища."""


class RedisStorage(BaseStorage):
    def __init__(self, redis_data: RedisData) -> None:
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
            unix_socket_path=self.redis_data.unix_socket_path, db=1
        )

    def save_state(self, key: str, value: Any) -> None:
        """Сохранить состояние в хранилище."""
        self.connection.set(key, value.encode())

    def retrieve_state(self, key: str) -> str | None:
        """Получить состояние из хранилища."""
        data = self.connection.get(key)
        return data.decode() if data else None

    def delete_state(self, key: str) -> None:
        return self.connection.delete(key)
