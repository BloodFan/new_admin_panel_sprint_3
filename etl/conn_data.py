from pydantic import Field
from pydantic_settings import BaseSettings


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


class ENVData(BaseSettings):
    periodicity: int
    schema_name: str
    batch_size: int


psql_data = PSQLData()
es_data = ESData()
redis_data = RedisData()
env_data = ENVData()
