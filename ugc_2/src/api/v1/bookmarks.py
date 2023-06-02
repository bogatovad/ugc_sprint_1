from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, HTTPException
from models.events import Bookmark
from services.bookmarks import BookmarkService, get_events_service
from core.config import logger
from core.error import DocumentExistsException

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
    try:
        await service.add_event(event)
    except DocumentExistsException:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)
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
