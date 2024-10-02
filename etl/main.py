import time
import os
from datetime import datetime
import redis
import elasticsearch

from postgresql_service import PostgresService
from etl_service import ETLService

dsl = {
    "dbname": os.environ.get("POSTGRES_DB", 'theatre'),
    "user": os.environ.get("POSTGRES_USER", 'postgres'),
    "password": os.environ.get("POSTGRES_PASSWORD", 'secret'),
    "host": os.environ.get("SQL_HOST"),
    "port": os.environ.get("SQL_PORT"),
}

tables = ['film_work', 'person', 'genre']
periodicity = 60
timestamp = str(datetime.min)


def test_redis():
    redis_client = redis.StrictRedis(
        unix_socket_path=os.environ.get("REDIS_UNIX_SOCKET_PATH"),
        db=1
    )
    redis_client.set('last_sync', str(datetime.now()))

    last_sync = redis_client.get('last_sync')
    if last_sync:
        print(f"Last Sync Time: {last_sync.decode('utf-8')}")


def main():
    print('START')
    while True:
        final_list: list = []
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
                [final_list.append(movie) for movie in result if movie not in final_list]
        validated_result = etl_service.transform(final_list)  # так стоп.... а как?
        print(len(validated_result))
        time.sleep(periodicity)


if __name__ == "__main__":
    main()
    # test_redis()
