from http import HTTPStatus

from core.config import logger
from fastapi import APIRouter, Depends, Request
from models.events import Bookmark
from services.bookmarks import BookmarkService, get_events_service

router = APIRouter()


@router.post(
    "/bookmarks",
    description="Положить фильм в закладки.",
)
async def add_bookmark(
    request: Request,
    event: Bookmark,
    service: BookmarkService = Depends(get_events_service),
):
    logger.info(f"request add bookmarks {request}")
    await service.add_event(event)
    return HTTPStatus.CREATED


@router.delete("/bookmarks", description="Убрать фильм из закладок.")
async def delete_bookmark(
    request: Request,
    event: Bookmark,
    service: BookmarkService = Depends(get_events_service),
):
    logger.info(f"request delete bookmarks {request}")
    result = await service.find_and_delete(event)
    if not result:
        return HTTPStatus.NOT_FOUND
    return HTTPStatus.NO_CONTENT
