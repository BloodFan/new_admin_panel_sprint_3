from typing import List

from elasticsearch import ConnectionError, Elasticsearch, TransportError, helpers
from elasticsearch.exceptions import (
    AuthenticationException,
    AuthorizationException,
    NotFoundError,
)
from my_backoff import backoff
from pydantic import BaseModel
from state_redis import state


class ESService:
    def __init__(
        self,
        connect_data: dict = None,
        index: str = None,
        batch_size=100,
        state_service=state,
    ) -> None:
        self.connect_data = connect_data
        self.index = index
        self.batch_size = batch_size
        self.state_service = state_service
        self.connection: Elasticsearch = self.get_es_connection()

    def transform_to_doc(self, data: list):
        for doc in data:
            action = {
                "_op_type": "index",
                "_index": self.index,
                "_id": str(doc.id),
                "_source": doc.dict(),
            }

            yield action

    def load(
        self,
        upload_data: List[BaseModel],
    ):
        actions = self.transform_to_doc(upload_data)

        batch, errors = helpers.bulk(
            client=self.connection,
            actions=actions,
            index=self.index,
            chunk_size=self.batch_size,
        )
        print(f"{batch=}")
        print(f"{errors=}")

    @backoff(
        errors=(ConnectionError, TransportError),
        client_errors=(AuthenticationException, AuthorizationException, NotFoundError),
    )
    def get_es_connection(self) -> Elasticsearch:
        """Создание соединения ES"""
        host = self.connect_data["es_host"]
        port = self.connect_data["es_port"]
        client = Elasticsearch(f"http://{host}:{port}")
        client.cluster.health(wait_for_status="yellow")
        return client

    def __enter__(self):
        if not self.connection or not self.connection.ping():
            self.connection = self.get_es_connection()
            print(f"{self.connection.ping()=}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.connection or not self.connection.ping():
            self.connection.close()
