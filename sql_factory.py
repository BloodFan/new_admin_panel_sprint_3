from abc import ABC, abstractmethod
import uuid
from typing import Set, List
import psycopg
from utils import batch_list
from queries import Queries


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
    ) -> List[dict]:
        if fw_ids:
            id_fw_str = ', '.join(f"'{str(uuid)}'" for uuid in fw_ids)  # сливаем множество в строку
            query = self.queries.result_query(id_fw_str=id_fw_str)  # запрос
        else:
            query = self.queries.result_query(timestamp=self.timestamp)  # запрос
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results


class ExtendedQueryHandler(BaseQueryHandler):
    def get_list_ids(self) -> List[uuid.UUID]:
        """
        Запрос  Person или Genre. list_ids

        Цикл while используется для порционного
        получения итогового результата.

        Итоговый результат получаем частями чтобы
        не загружать БД одним большим запросом.
        """
        person_ids: list = []  # обьявлен итоговый список

        current_timestamp = self.timestamp  # записываем изначальный modified в переменную для дальнейшей перезаписи

        try:
            while True:
                query = self.queries.get_list_ids(
                    schema_name=self.schema_name,
                    current_timestamp=current_timestamp,
                    batch_size=self.batch_size,
                    table_name=self.table_name
                )  # запрос

                self.cursor.execute(query)
                results = self.cursor.fetchall()

                if not results:  # если запрос пуст прерываем цикл while
                    break

                ids = [item['id'] for item in results]   # список из UUID
                # 'id': UUID('10136fb4-e296-4bdd-bc02-af3abd90a0e9')
                person_ids.extend(ids)  # добавляем ids в общий результат

                current_timestamp = results[-1]['modified']  # перезапись что бы не тащить одинаковые записи
            return person_ids
        except psycopg.Error as e:
            print(f"Ошибка при извлечении данных: {e}")

    def get_film_work_ids(
            self,
            list_ids: List[uuid.UUID],
            table_name: str,
    ) -> Set[uuid.UUID]:
        """
        Запрос из film_work.
        Для фильтрации pfw получает строку из списка person_id.
        Для фильтрации gfw получает строку из списка genre_id.

        Для сопоставления film_work <-> person | genre
        используем смежную таблицу person_film_work(pfw) | genre_film_work(gfw).
        """
        fw_ids = set()
        try:
            # делим person_ids на срезы для дробления запроса
            for batch in batch_list(list_ids, self.batch_size):
                id_list_str = ', '.join(f"'{str(uuid)}'" for uuid in batch)  # -> в строку для передачи query

                query = self.queries.get_film_work_ids(
                    schema_name=self.schema_name,
                    id_list_str=id_list_str,
                    table_name=table_name,
                )  # запрос в БД

                self.cursor.execute(query)
                results = self.cursor.fetchall()

                ids = {item['id'] for item in results}
                fw_ids.update(ids)
                # Проблема: запрос возвращает  дублирующие записи film_work
                # set потому что запросы возвращают дублирующие записи
            return fw_ids

        except (Exception, psycopg.Error) as e:
            print(f"Ошибка при извлечении данных: {e}")


class FilmWorkQueryHandler(BaseQueryHandler):
    table_name: str = 'film_work'

    def get_result_query(self):
        return self.result_query()


class PersonFilmWorkQueryHandler(ExtendedQueryHandler):
    table_name: str = 'person'
    m2m_table_name: str = 'person_film_work'

    def get_result_query(self):
        person_ids = self.get_list_ids()
        fw_ids = self.get_film_work_ids(
            person_ids, table_name=self.m2m_table_name
        )
        return self.result_query(fw_ids)


class GenreFilmWorkQueryHandler(ExtendedQueryHandler):
    table_name: str = 'genre'
    m2m_table_name: str = 'genre_film_work'

    def get_result_query(self):
        genre_ids = self.get_list_ids()
        fw_ids = self.get_film_work_ids(
            genre_ids, table_name=self.m2m_table_name
        )
        return self.result_query(fw_ids)
