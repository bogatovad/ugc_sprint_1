from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn
from core.config import settings

from api.v1.views import router


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)
app.include_router(router, prefix='/api/v1', tags=['views'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.host,
        port=settings.port,
        reload=True,
    )