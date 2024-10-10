from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .core import config
from .db.elastic import get_elastic
from .db.redis import get_redis
from .api.v1 import films

# Вроде как более современный аналог для @app.on_event('startup') и @app.on_event('shutdown')
# но это не точно)

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await get_redis()
    elastic = await get_elastic()

    # Передача объектов в контекст
    app.state.redis = redis
    app.state.elastic = elastic

    # Ожидание до конца контекста
    yield

    # Закрытие соединений
    await redis.close()
    await elastic.close()

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
