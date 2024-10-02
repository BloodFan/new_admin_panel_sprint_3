import time
from datetime import datetime
from pprint import pprint

from postgresql_service import PostgresService
from etl_service import ETLService


dsl = {
    "dbname": 'theatre',
    "user": 'postgres',
    "password": 'secret',
    "host": '127.0.0.1',
    "port": '5432',
}

tables = ['film_work', 'person', 'genre']
periodicity = 60
timestamp = str(datetime.min)


def main():
    while True:
        for table in tables:
            with PostgresService(
                connect_data=dsl,
                schema_name='content',
                batch_size=100,
                timestamp=timestamp
            ) as psql_service:
                etl_service = ETLService(psql_service)
                # etl_service.process()
                result = etl_service.extract(table)
                validated_result = etl_service.transform(result)
                print(len(validated_result))
                # перед transform наверное имеет смысл объеденить результаты

        time.sleep(periodicity)


if __name__ == "__main__":
    main()
