# Заключительное задание первого модуля

Ваша задача в этом уроке — загрузить данные в Elasticsearch из PostgreSQL. Подробности задания в папке `etl`.

main.py - точка запуска.
dir state:
	state_class.py -реализация состояния(мое решение)
	state_redis.py - псевдо-реализация класса состояния на основе redis(мое решение)
	state_redis_test.py - тестирование state_redis

etl_service.py - общий сервис ETL

models.py - для валидации документа ES в pydantic
movies.json - Индекс ES

my_backoff.py - реализация декоратора my_backoff (мое решение)

postgresql_service.py - экстрактор из PSQL
queries.py - SQL-запросы в БД

sql_factory.py - фабричные классы для postgresql_service
extract_result.py - пример извлеченного результата.

Вопросы:
если поле directors_names не содержит значение(None) корректно ли его отработает ES?