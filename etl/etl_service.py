from typing import List
import psycopg

from models import Movie
from postgresql_service import PostgresService


class ETLService:
    def __init__(
            self,
            psql_service: PostgresService = None,
            batch_size: int = 100,
    ) -> None:
        self.psql_service = psql_service
        self.batch_size = batch_size
        self.psql_cursor: psycopg.Cursor = None

    def process(self):
        """запускать внутренние компоненты."""
        # self.psql_cursor = self.plsql_service.create_cursor()

    def extract(self, table: str):
        """Извлекает данные из PosgreSQL"""
        return self.psql_service.handler(table)

    def transform(self, movies_list: List[dict]) -> List[Movie]:
        """
        Преобразование формата данных
        PosgreSQL -> Elasticsearch
        """
        return [Movie(**movie) for movie in movies_list]


    def load(self):
        """загрузка полученных данных в Elasticsearch"""
        pass
