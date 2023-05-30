import uvicorn
from api.v1.bookmarks import router as bookmarks_router
from api.v1.likes import router as likes_router
from api.v1.reviews import router as reviews_router
from core.config import settings
from db import mongodb
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    mongodb.mongo_client = AsyncIOMotorClient(
        f"mongodb://{settings.mongo_host}:{settings.mongo_port}/"
    )


app.include_router(likes_router, prefix="/api/v1", tags=["likes"])
app.include_router(bookmarks_router, prefix="/api/v1", tags=["bookmarks"])
app.include_router(reviews_router, prefix="/api/v1", tags=["reviews"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
