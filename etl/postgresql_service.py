from typing import Optional
import psycopg
from psycopg.rows import dict_row
from psycopg import connection as _connection, ClientCursor

from queries import Queries
from sql_factory import (FilmWorkQueryHandler,
                         PersonFilmWorkQueryHandler,
                         GenreFilmWorkQueryHandler)


def query_handlers(table_name: str):
    data = {
        'film_work': FilmWorkQueryHandler,
        'person': PersonFilmWorkQueryHandler,
        'genre': GenreFilmWorkQueryHandler
    }
    return data[table_name]


class PostgresService:

    def __init__(
        self,
        connect_data: dict = None,
        schema_name: Optional[str] = None,
        batch_size: int = 100,
        timestamp: str = None,
        queries: Queries = Queries()
    ) -> None:
        self.connect_data = connect_data
        self.schema_name = schema_name
        self.batch_size = batch_size
        self.timestamp = timestamp
        self.queries = queries
        self.connection: _connection = self.get_psql_connection()
        self.cursor: psycopg.Cursor = self.create_cursor()

    def create_cursor(
        self,
    ) -> psycopg.Cursor:
        if not self.connection:
            raise RuntimeError(
                "Соединение с базой данных(PostgreSQL) не установлено!"
            )
        return self.connection.cursor()

    def close_cursor(self, p_cursor: psycopg.Cursor) -> None:
        return p_cursor.close()

    def get_psql_connection(self) -> _connection:
        """Создание соединения psql"""
        return psycopg.connect(
            **self.connect_data,
            row_factory=dict_row,
            cursor_factory=ClientCursor
        )

    def handler(self, table: str):
        handler = query_handlers(table)
        handle = handler(
            self.cursor,
            self.queries,
            self.timestamp,
            self.schema_name,
            self.batch_size
        )
        return handle.get_result_query()

    def __enter__(self):
        if not self.connection or self.connection.closed:
            self.connection = self.get_psql_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and not self.connection.closed:
            self.connection.close()
