from state_class import BaseStorage
from typing import Any, Dict
import json


class RedisStorage(BaseStorage):
    def __init__(self, db) -> None:
        self.db = db
        self.validate_data()

    def validate_data(self,):
        data = self.db.data
        for key in data:
            try:
                _ = json.loads(data[key])

            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(
                    "Ошибка декодирования JSON", e.doc, e.pos
                )

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        for key, value in state.items():
            json_value = json.dumps({key: value})
            self.db.set(name='data', value=json_value)

    def retrieve_state(self, name: str) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        for value in self.db.data.values():
            parsed_data = json.loads(value)
            return parsed_data[name]