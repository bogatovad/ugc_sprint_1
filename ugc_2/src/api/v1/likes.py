from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, HTTPException
from models.events import Like
from services.likes import UserLikeService, get_events_service
from core.config import logger
from core.error import DocumentExistsException


router = APIRouter()


@router.post(
    "/likes",
    description="Поставить лайк фильму.",
)
async def add_like(
    request: Request,
    event: Like,
    service: UserLikeService = Depends(get_events_service),
):
    logger.info(f"request add like {request}")
    try:
        await service.add_event(event)
    except DocumentExistsException:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)
    return HTTPStatus.CREATED


@router.delete("/likes", description="Убрать лайк")
async def delete_like(
    request: Request,
    event: Like,
    service: UserLikeService = Depends(get_events_service),
):
    logger.info(f"request delete like {request}")
    result = await service.find_and_delete(event)
    return HTTPStatus.NO_CONTENT if result else HTTPStatus.NOT_FOUND
