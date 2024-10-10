
`main.py` - точка запуска.

## Задачей сервиса является процесс ETL(extract->transform->load) между сервисами(db(PostgreSQL)->elasticsearch)

## Инициализирующие данные находятся в  /etl/index_data.py и собраны в словарь indexs_dict
- **indexs_dict:**
  - **'model':** - Тип модели для валидации объектов через pydantic
  - **'index':** - Название индекса elasticsearch(адрес файлов: /docker/dev/es/)
  - **'query_handlers':** - ключи обработчиков извлечения данных для def query_handlers(postgresql_service.py)


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
