import time

from conn_data import env_data, es_data, psql_data, redis_data
from es_service import ESService
from etl_service import ETLService
from loggers import setup_logger
from models import Movie
from my_types import ServiceType
from postgresql_service import PostgresService
from state_redis import RedisStorage, State

logger = setup_logger("load_data.log")


def main():
    logger.info("Активация сервисов.")
    storage = RedisStorage(redis_data)
    state_service = State(storage=storage)

    psql_service = PostgresService(
        connect_data=psql_data,
        schema_name=env_data.schema_name,
        batch_size=env_data.batch_size,
        state_service=state_service,
    )
    es_service = ESService(
        connect_data=es_data, index=env_data.index, state_service=state_service
    )

    etl_service = ETLService()
    etl_service.config(ServiceType.STATE, state_service)
    etl_service.config(ServiceType.POSTGRESQL, psql_service)
    etl_service.config(ServiceType.ELASTICSEARCH, es_service)

    logger.info("Старт цикла")
    while True:
        final_list: list = []
        for table in env_data.tables:
            with etl_service.psql_service:
                result = etl_service.extract(table)
                for obj in result:
                    if obj not in final_list:
                        final_list.append(obj)
        logger.info("Данные извлечены.")
        transform_list, last_m = etl_service.transform(final_list, Movie)
        logger.info("Данные преобразованы.")
        with etl_service.es_service:
            etl_service.load_to_es(transform_list, last_m)
        logger.info("Данные загружены в ElasticSearch.")
        time.sleep(env_data.periodicity)


if __name__ == "__main__":
    main()
