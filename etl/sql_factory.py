import uuid
from abc import ABC, abstractmethod
from typing import Any, Generator, Set

import psycopg
import psycopg.sql
from loggers import setup_logger
from queries import Queries
from utils import batch_list

logger = setup_logger("load_data.log")


class BaseQueryHandler(ABC):
    def __init__(
        self,
        cursor: psycopg.Cursor,
        queries: Queries,
        timestamp: str,
        schema_name: str,
        batch_size: int,
    ) -> None:
        self.timestamp = timestamp
        self.cursor = cursor
        self.queries = queries
        self.schema_name = schema_name
        self.batch_size = batch_size

    @abstractmethod
    def get_result_query(self):
        pass

    def result_query(
        self,
        fw_ids: Set[uuid.UUID] = None,
    ) -> Generator[dict, Any, Any]:
        self.cursor.itersize = 100
        if fw_ids:
            query = self.queries.result_query(id_fw_list=list(fw_ids))
            self.cursor.execute(query, (list(fw_ids),))
        else:
            query = self.queries.result_query(timestamp=self.timestamp)
            self.cursor.execute(query, (self.timestamp,))
        for row in self.cursor:
            yield row


class ExtendedQueryHandler(BaseQueryHandler):
    def get_list_ids(self) -> list[uuid.UUID]:
        """
        Запрос  Person или Genre. list_ids

        Цикл while используется для порционного
        получения итогового результата.

        Итоговый результат получаем частями чтобы
        не загружать БД одним большим запросом.
        """
        person_ids: list = []

        current_timestamp = self.timestamp

        try:
            while True:
                query = self.queries.get_list_ids(
                    schema_name=self.schema_name,
                    table_name=self.table_name,
                )

                self.cursor.execute(
                    query, (current_timestamp, self.batch_size)
                )
                results = self.cursor.fetchall()

                if not results:
                    break

                ids = [item["id"] for item in results]
                person_ids.extend(ids)

                current_timestamp = results[-1]["modified"]
            return person_ids
        except psycopg.Error as e:
            logger.error(f"Ошибка при извлечении данных: {e}")

    def get_film_work_ids(
        self,
        list_ids: list[uuid.UUID],
        table_name: str,
    ) -> Set[uuid.UUID]:
        """
        Запрос из film_work.
        Для фильтрации pfw получает строку из списка person_id.
        Для фильтрации gfw получает строку из списка genre_id.

        Для сопоставления film_work <-> person | genre
        используем смежную таблицу
        person_film_work(pfw) | genre_film_work(gfw).
        """
        fw_ids = set()
        try:
            for batch in batch_list(list_ids, self.batch_size):
                batch_ids = (str(uuid) for uuid in batch)

                query = self.queries.get_film_work_ids(
                    schema_name=self.schema_name,
                    table_name=table_name,
                )

                self.cursor.execute(query, (batch_ids,))
                results = self.cursor.fetchall()

                ids = {item["id"] for item in results}
                fw_ids.update(ids)
            return fw_ids

        except (Exception, psycopg.Error) as e:
            logger.error(f"Ошибка при извлечении данных: {e}")


class FilmWorkQueryHandler(BaseQueryHandler):
    table_name: str = "film_work"

    def get_result_query(self):
        return self.result_query()


class PersonFilmWorkQueryHandler(ExtendedQueryHandler):
    table_name: str = "person"
    m2m_table_name: str = "person_film_work"

    def get_result_query(self):
        person_ids = self.get_list_ids()
        fw_ids = self.get_film_work_ids(
            person_ids, table_name=self.m2m_table_name
        )
        return self.result_query(fw_ids)


class GenreFilmWorkQueryHandler(ExtendedQueryHandler):
    table_name: str = "genre"
    m2m_table_name: str = "genre_film_work"

    def get_result_query(self):
        genre_ids = self.get_list_ids()
        fw_ids = self.get_film_work_ids(
            genre_ids, table_name=self.m2m_table_name
        )
        return self.result_query(fw_ids)
