# Заключительное задание первого модуля

Ваша задача в этом уроке — загрузить данные в Elasticsearch из PostgreSQL. Подробности задания в папке `etl`.

`main.py` - точка запуска.

## Структура директорий

- **dir docker:**
  - **dir dev:**
    - конфигурационные файлы для `docker-compose.yml`

## Описание файлов

- **etl_service.py:** общий сервис ETL.
- **es_service.py:** Loader ES.
- **postgresql_service.py:** экстрактор из PSQL.
- **state_redis.py:** сервис состояния.

- **sql_factory.py:** фабричные классы для `postgresql_service`
- **queries.py:** SQL-запросы в БД

- **models.py:** для валидации `pydantic`
- **movies.json:** Индекс ES
- **my_backoff.py:** реализация декоратора `backoff` (мое решение)
- **conn_data.py:** конфигурации для доступа (Redis, ElasticSearch, PostgreSQL)
- **index_data.py:** конфигурации для цикла(ключи для query_handlers, модель и индекс)
- **loggers.py:** настройки логгера
