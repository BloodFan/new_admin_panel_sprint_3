# Заключительное задание первого модуля

Ваша задача в этом уроке — загрузить данные в Elasticsearch из PostgreSQL. Подробности задания в папке `etl`.

main.py - точка запуска.

dir docker:
	dir dev:
		- конфигурационные файлы для docker-compose.yml


etl_service.py - общий сервис ETL
es_service.py - Loader ES

models.py - для валидации документа ES в pydantic
movies.json - Индекс ES

my_backoff.py - реализация декоратора backoff (мое решение)

postgresql_service.py - экстрактор из PSQL
sql_factory.py - фабричные классы для postgresql_service
queries.py - SQL-запросы в БД

conn_data.py - конфигурации для доступа(Redis, ElasticSearch, PostrgeSql)

loggers.py - настройки логгера