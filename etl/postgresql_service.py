from types import TracebackType
from typing import Type

import psycopg
from conn_data import PSQLData
from my_backoff import backoff
from psycopg import (ClientCursor, IntegrityError, InterfaceError,
                     OperationalError, ProgrammingError)
from psycopg import connection as _connection
from psycopg.rows import dict_row
from queries import Queries
from sql_factory import (FilmWorkQueryHandler, GenreFilmWorkQueryHandler,
                         PersonFilmWorkQueryHandler, GenreQueryHandler,
                         PersonQueryHandler)
from state_redis import State


def query_handlers(table_name: str):
    data = {
        "film_work": FilmWorkQueryHandler,
        "person": PersonFilmWorkQueryHandler,
        "genre": GenreFilmWorkQueryHandler,
        "genre_index": GenreQueryHandler,
        'person_index': PersonQueryHandler
    }
    return data[table_name]


class PostgresService:

    def __init__(
        self,
        connect_data: PSQLData = None,
        schema_name: str | None = None,
        batch_size: int = 100,
        state_service: State = None,
        queries: Queries = Queries(),
        connection: _connection = None,
    ) -> None:
        self.connect_data = connect_data
        self.schema_name = schema_name
        self.batch_size = batch_size
        self.state_service = state_service
        self.queries = queries
        self.connection = connection

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

    @backoff(
        errors=(OperationalError, InterfaceError),
        client_errors=(ProgrammingError, IntegrityError),
    )
    def get_psql_connection(self) -> _connection:
        """Создание соединения psql"""
        return psycopg.connect(
            **self.connect_data.model_dump(),
            row_factory=dict_row,
            cursor_factory=ClientCursor
        )

    def handler(self, handler: str, timestamp: str):
        handler = query_handlers(handler)
        handle = handler(
            self.cursor,
            self.queries,
            timestamp,
            self.schema_name,
            self.batch_size,
        )
        return handle.get_result_query()

    def __enter__(self):
        if not self.connection or self.connection.closed:
            self.connection: _connection = self.get_psql_connection()
            self.cursor: psycopg.Cursor = self.create_cursor()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        if self.connection and not self.connection.closed:
            self.connection.close()
