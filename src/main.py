import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.views import router
from core.config import settings
from db.kafka_producer import producer

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
def start_producer():
    producer.start()


@app.on_event('shutdown')
def stop_producer():
    producer.stop()


app.include_router(router, prefix='/api/v1', tags=['views'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.host,
        port=settings.port,
        reload=True,
    )
