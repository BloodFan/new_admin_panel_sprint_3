import os

psql_data = {
    "dbname": os.environ.get("POSTGRES_DB", "theatre"),
    "user": os.environ.get("POSTGRES_USER", "postgres"),
    "password": os.environ.get("POSTGRES_PASSWORD", "secret"),
    "host": os.environ.get("SQL_HOST"),
    "port": os.environ.get("SQL_PORT"),
}
es_data = {
    "es_host": os.environ.get("ES_HOST"),
    "es_port": os.environ.get("ES_PORT"),
}
redis_data = {"unix_socket_path": os.environ.get("REDIS_UNIX_SOCKET_PATH")}
