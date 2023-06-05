import uvicorn
from api.v1.bookmarks import router as bookmarks_router
from api.v1.likes import router as likes_router
from api.v1.reviews import router as reviews_router
from core.config import settings
from db import mongodb
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from motor.motor_asyncio import AsyncIOMotorClient

import sentry_sdk


sentry_sdk.init(
    dsn="https://c61890820d1149d8a3d17f062e92404c@o570611.ingest.sentry.io/4505269445263360",
    traces_sample_rate=1.0,
)

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

@AuthJWT.load_config
def get_config():
    return settings


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.on_event("startup")
async def startup():
    mongodb.mongo_client = AsyncIOMotorClient(
        f"mongodb://{settings.mongo_host}:{settings.mongo_port}/"
    )


app.include_router(likes_router, prefix="/api/v1", tags=["likes"])
app.include_router(bookmarks_router, prefix="/api/v1", tags=["bookmarks"])
app.include_router(reviews_router, prefix="/api/v1", tags=["reviews"])


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
