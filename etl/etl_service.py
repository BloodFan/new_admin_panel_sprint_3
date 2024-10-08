from datetime import datetime
from typing import Union

from es_service import ESService
from models import BaseModel
from my_types import ServiceType
from postgresql_service import PostgresService
from state_redis import State


class ETLService:
    def __init__(
        self,
        psql_service: PostgresService = None,
        es_service: ESService = None,
        batch_size: int = 100,
        state_service: State = None,
    ) -> None:
        self.psql_service = psql_service
        self.es_service = es_service
        self.batch_size = batch_size
        self.state_service = state_service

    def config(
        self,
        type_process: ServiceType,
        launc_process: Union[PostgresService, ESService, State],
    ) -> None:
        """запускает внутренние компоненты."""
        if type_process == ServiceType.POSTGRESQL:
            self.psql_service = launc_process
        if type_process == ServiceType.ELASTICSEARCH:
            self.es_service = launc_process
        if type_process == ServiceType.STATE:
            self.state_service = launc_process

    def extract(self, handler: str, model: BaseModel):
        """Извлекает данные из PosgreSQL"""
        timestamp = self.state_service.get_state(
            f"timestamp_{model.__name__}", default=str(datetime.min)
        )
        return self.psql_service.handler(handler, timestamp)

    def validave_data(
        self, model: BaseModel, object_list: list[dict]
    ) -> list[BaseModel]:
        """Валидация данных через модель pydantic."""
        return [model(**object) for object in object_list]

    def transform(self, _list: list, model: BaseModel):
        """
        Преобразование формата данных
        PosgreSQL -> Elasticsearch
        """
        last_m = self.state_service.get_state(
            key=f"timestamp_{model.__name__}"
        )
        transform_list = []

        for obj in _list:
            modified = obj["modified"]
            if last_m is None:
                last_m = modified
            elif modified > last_m:
                last_m = modified
            del obj["modified"]
            transform_list.append(model(**obj))
        return transform_list, last_m

    def load_to_es(
            self, upload_data: list[BaseModel], last_m: str, model: BaseModel
    ):
        """загрузка полученных данных в Elasticsearch"""
        self.es_service.load(upload_data)
        self.state_service.set_state(
            key=f"timestamp_{model.__name__}", value=str(last_m)
        )
