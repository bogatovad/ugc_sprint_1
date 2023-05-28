from http import HTTPStatus

from fastapi import APIRouter, Depends, Request

from models.events import Bookmark
from services.bookmarks import BookmarkService, get_events_service


router = APIRouter()


@router.post(
    "/bookmarks",
    description="Положить фильм в закладки.",
)
async def add_bookmark(
    request: Request, event: Bookmark, service: BookmarkService = Depends(get_events_service)
):
    await service.add_event(event)
    return HTTPStatus.CREATED


@router.delete(
    "/bookmarks",
    description="Убрать фильм из закладок."
)
async def delete_bookmark(
    request: Request, event: Bookmark, service: BookmarkService = Depends(get_events_service)
):
    result = await service.delete(event)
    if not result:
        return HTTPStatus.NOT_FOUND
    return HTTPStatus.NO_CONTENT