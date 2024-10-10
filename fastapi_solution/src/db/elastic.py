from elasticsearch import AsyncElasticsearch
from src.core.config import es_data

es: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch:
    return AsyncElasticsearch(
        hosts=[f'{es_data.es_schema}{es_data.es_host}:{es_data.es_port}']
    )
