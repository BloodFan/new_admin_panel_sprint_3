from typing import Optional


class Queries:

    @staticmethod
    def get_list_ids(
        schema_name: str,
        current_timestamp: str,
        batch_size: int,
        table_name: str,
    ) -> str:
        """
        Запрос Person или Genre.
        Фильтрация по modified.
        порядок по modified.
        возвращает фиксированное кол-во.
        """

        return f"""
            SELECT id, modified
            FROM {schema_name}.{table_name}
            WHERE modified > '{current_timestamp}'
            ORDER BY modified
            LIMIT {batch_size};
        """

    @staticmethod
    def get_film_work_ids(
        schema_name: str,
        id_list_str: str,
        table_name: str,
    ) -> str:
        """
        Запрос из film_work.
        Для фильтрации pfw получает строку из списка person_id.
        Для фильтрации gfw получает строку из списка genre_id.
        Для сопоставления film_work <-> person | genre
        используем смежную таблицу person_film_work(pfw) | genre_film_work(gfw)

        В Архитектура ETL предложено использовать LEFT JOIN
        но разве не разумнее INNER?

        проблема с дубликатами: добавить GROUP BY fw.id? но запросов все равно несколько
        """
        if table_name == 'person_film_work':
            join_and_filter = f"""
            LEFT JOIN {schema_name}.{table_name} pfw
            ON fw.id = pfw.film_work_id
            WHERE pfw.person_id IN ({id_list_str})
        """
        if table_name == 'genre_film_work':
            join_and_filter = f"""
            LEFT JOIN {schema_name}.{table_name} gfw
            ON fw.id = gfw.film_work_id
            WHERE gfw.genre_id IN ({id_list_str})
        """
        return f"""
            SELECT fw.id, fw.modified
            FROM {schema_name}.film_work fw
            {join_and_filter}
            ORDER BY fw.modified;
        """

    @staticmethod
    def result_query(
        id_fw_str: Optional[str] = None,
        timestamp: Optional[str] = None
    ) -> str:
        """
        Результирующий запрос.

        Фильтрация  для film_work по fw.modified > '<время>'.

        Фильтрация  для person and genre по fw.id
        передаваемому списку id_fw_str(строка через ,).
        """
        if id_fw_str:
            filter = f"WHERE fw.id IN ({id_fw_str})"
        if timestamp:
            filter = f"WHERE fw.modified > '{timestamp}'"
        return (
            f"""SELECT
                    fw.id AS id,
                    fw.rating AS imdb_rating,
                    fw.title,
                    fw.description,
                    array_to_string(array_agg(DISTINCT g.name), ', ') AS genres,
                    array_to_string(
                        array_agg(
                            DISTINCT p.full_name
                        ) FILTER (WHERE pfw.role = 'director'), ', '
                    ) AS directors_names,
                    array_to_string(
                        array_agg(
                            DISTINCT p.full_name
                        ) FILTER (WHERE pfw.role = 'actor'), ', '
                    ) AS actors_names,
                    array_to_string(
                        array_agg(
                            DISTINCT p.full_name
                        ) FILTER (WHERE pfw.role = 'writer'), ', '
                    ) AS writers_names,
                    array_agg(
                        DISTINCT jsonb_build_object(
                            'id', p.id, 'name', p.full_name
                        )
                    ) FILTER (WHERE pfw.role = 'director') AS directors,
                    array_agg(
                        DISTINCT jsonb_build_object(
                            'id', p.id, 'name', p.full_name
                        )
                    ) FILTER (WHERE pfw.role = 'actor') AS actors,
                    array_agg(
                        DISTINCT jsonb_build_object(
                            'id', p.id, 'name', p.full_name
                        )
                    ) FILTER (WHERE pfw.role = 'writer') AS writers
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                {filter}
                GROUP BY fw.id; """
        )
