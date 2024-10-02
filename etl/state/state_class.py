import abc
import json
from typing import Any, Dict
from json import JSONDecodeError


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния.

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""

    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""


class JsonFileStorage(BaseStorage):
    """Реализация хранилища, использующего локальный файл.

    Формат хранения: JSON
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(state, file, ensure_ascii=False, indent=4)
        except TypeError as e:
            print(f"Ошибка сериализации: {e}")

    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                if isinstance(data, dict):
                    return data if data else {}
                return {}

        except (json.JSONDecodeError, FileNotFoundError):
            return {}


class State:
    """Класс для работы с состояниями."""

    def __init__(
            self,
            storage: BaseStorage = None,
    ) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        self.storage.save_state(state={key: value})

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        try:
            return self.storage.retrieve_state(key)
        except JSONDecodeError as e:
            raise JSONDecodeError(f"{e}")


# state = State()
# state.set_state('key_1', 'value_1')

# state.get_state('key_1')
