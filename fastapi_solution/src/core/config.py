import os
from logging import config as logging_config
from pydantic_settings import BaseSettings

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')


class ESData(BaseSettings):
    es_schema: str
    es_host: str
    es_port: str


class RedisData(BaseSettings):
    unix_socket_path: str

    class Config:
        env_prefix = "REDIS_"
        envenv_file = ".conn.env"


es_data = ESData()
redis_data = RedisData()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
