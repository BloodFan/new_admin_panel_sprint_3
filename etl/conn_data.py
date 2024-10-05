import os

from pydantic import Field
from pydantic_settings import BaseSettings

from models import ENVData


class PSQLData(BaseSettings):
    dbname: str = Field(default="theatre", env="POSTGRES_DB")
    user: str = Field(default="postgres", env="POSTGRES_USER")
    password: str = Field(default="secret", env="POSTGRES_PASSWORD")
    host: str
    port: str

    class Config:
        env_prefix = "SQL_"
        envenv_file = ".conn.env"


class ESData(BaseSettings):
    es_host: str
    es_port: str


class RedisData(BaseSettings):
    unix_socket_path: str

    class Config:
        env_prefix = "REDIS_"
        envenv_file = ".conn.env"


env_data = {
    "tables": os.environ.get("TABLES"),
    "periodicity": os.environ.get("PERIODICITY"),
    "schema_name": os.environ.get("SCHEMA_NAME"),
    "index": os.environ.get("INDEX"),
    "batch_size": os.environ.get("BATCH_SIZE"),
}

psql_data = PSQLData()
es_data = ESData()
redis_data = RedisData()
env_data = ENVData(**env_data)
