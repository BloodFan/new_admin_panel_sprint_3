import time
from datetime import datetime

from conn_data import es_data, psql_data
from es_service import ESService
from etl_service import ETLService
from models import Movie
from my_types import ServiceType
from postgresql_service import PostgresService
from state_redis import state

tables = ["film_work", "person", "genre"]
periodicity = 60

timestamp = datetime.min


def main():
    etl_service = ETLService(state=state)
    while True:
        timestamp = state.get_state(key="timestamp")
        if timestamp is None:
            timestamp = datetime.min
        final_list: list = []
        for table in tables:
            with PostgresService(
                connect_data=psql_data,
                schema_name="content",
                batch_size=100,
                timestamp=str(timestamp),
            ) as psql_service:
                etl_service.config(ServiceType.POSTGRESQL, psql_service)
                result = etl_service.extract(table)
                for movie in result:
                    if movie not in final_list:
                        final_list.append(movie)
        transform_list, last_m = etl_service.transform(final_list, Movie)
        with ESService(connect_data=es_data, index="movies") as es_service:
            etl_service.config(ServiceType.ELASTICSEARCH, es_service)
            etl_service.load_to_es(transform_list, last_m)
        time.sleep(periodicity)


if __name__ == "__main__":
    main()
