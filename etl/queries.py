from psycopg import sql


class Queries:

    @staticmethod
    def get_list_ids(
        schema_name: str,
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
            WHERE modified > %s
            ORDER BY modified
            LIMIT %s;
        """

    @staticmethod
    def get_film_work_ids(
        schema_name: str,
        table_name: str,
    ) -> str:
        """
        Запрос из film_work.
        Для фильтрации pfw получает строку из списка person_id.
        Для фильтрации gfw получает строку из списка genre_id.
        Для сопоставления film_work <-> person | genre
        используем смежную таблицу person_film_work(pfw) | genre_film_work(gfw)
        """
        if table_name == "person_film_work":
            join = (
                f"LEFT JOIN {schema_name}.{table_name} "
                "pfw ON fw.id = pfw.film_work_id"
            )
            where = "WHERE pfw.person_id IN %s"

        elif table_name == "genre_film_work":
            join = (
                f"LEFT JOIN {schema_name}.{table_name} "
                "gfw ON fw.id = gfw.film_work_id"
            )
            where = "WHERE gfw.genre_id IN %s"

        return f"""
            SELECT fw.id, fw.modified
            FROM {schema_name}.film_work fw
            {join}
            {where}
            ORDER BY fw.modified;
        """

    @staticmethod
    def result_query(
        id_fw_list: list[str] | None = None, timestamp: str | None = None
    ) -> sql.Composed:
        """
        Результирующий запрос.

        Фильтрация для film_work по fw.modified > '<время>'.

        Фильтрация для person и genre по fw.id
        передаваемому списку id_fw_list (строка через ',').
        """
        if id_fw_list is not None:
            _filter = sql.SQL("WHERE fw.id = ANY(%s)")
        elif timestamp is not None:
            _filter = sql.SQL("WHERE fw.modified > %s")

        return sql.SQL(
            """SELECT
                fw.id AS id,
                fw.rating AS imdb_rating,
                fw.title,
                fw.description,
                GREATEST(fw.modified, MAX(p.modified),
                    MAX(g.modified)) AS modified,
                array_agg(DISTINCT g.name) AS genres,
                array_agg(DISTINCT p.full_name)
                    FILTER (WHERE pfw.role = 'director')
                    AS directors_names,
                array_agg(DISTINCT p.full_name)
                    FILTER (WHERE pfw.role = 'actor')
                    AS actors_names,
                array_agg(DISTINCT p.full_name)
                    FILTER (WHERE pfw.role = 'writer')
                    AS writers_names,
                array_agg(DISTINCT jsonb_build_object(
                    'id', p.id,
                    'name', p.full_name))
                    FILTER (WHERE pfw.role = 'director')
                    AS directors,
                array_agg(DISTINCT jsonb_build_object(
                    'id', p.id,
                    'name', p.full_name))
                    FILTER (WHERE pfw.role = 'actor')
                    AS actors,
                array_agg(DISTINCT jsonb_build_object(
                    'id', p.id,
                    'name', p.full_name))
                    FILTER (WHERE pfw.role = 'writer')
                    AS writers
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw
                ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p
                ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw
                ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g
                ON g.id = gfw.genre_id
            {}
            GROUP BY fw.id;""").format(_filter)

    @staticmethod
    def get_genres(
        schema_name: str,
        table_name: str,
    ) -> str:
        """Запрос Genre."""

        return f"""
            SELECT id, name, modified
            FROM {schema_name}.{table_name}
            WHERE modified > %s
            ORDER BY modified;
        """

    @staticmethod
    def get_persons(
        schema_name: str,
        table_name: str,
        m2m_table: str,
    ) -> str:
        """Запрос person. """
        return f"""
            SELECT
                p.id,
                p.full_name,
                p.modified,
                array_agg(DISTINCT jsonb_build_object(
                    'role', pfw.role,
                    'film_work_id', fw.id,
                    'film_work_title', fw.title))
                    AS participated
            FROM
                {schema_name}.{table_name} p
            LEFT JOIN {schema_name}.{m2m_table} pfw
                ON p.id = pfw.person_id
            LEFT JOIN {schema_name}.film_work fw
                ON pfw.film_work_id = fw.id
            WHERE
                p.modified > %s
            GROUP BY
                p.id
            ORDER BY
                p.id;
        """
