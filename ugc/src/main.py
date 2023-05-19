import uvicorn
from aiokafka import AIOKafkaProducer
from api.v1.views import router
from core.config import settings
from db import kafka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def start_producer():
    kafka.kafka = AIOKafkaProducer(
        bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}"
    )
    kafka.kafka.client.add_topic(settings.kafka_topic)
    await kafka.kafka.start()


@app.on_event("shutdown")
async def stop_producer():
    await kafka.kafka.stop()


app.include_router(router, prefix="/api/v1", tags=["views"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
