from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi_jwt_auth import AuthJWT
from models.events import Bookmark, Event
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
    event: Event,
    Authorize: AuthJWT = Depends(),
    service: BookmarkService = Depends(get_events_service),
):
    logger.info(f"request add bookmarks {request}")
    Authorize.fresh_jwt_required()
    user_id = Authorize.get_jwt_subject()
    try:
        await service.add_event(Bookmark(user_id=user_id, movie_id=event.movie_id))
    except DocumentExistsException:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)
    return HTTPStatus.CREATED


@router.delete("/bookmarks", description="Убрать фильм из закладок.")
async def delete_bookmark(
    request: Request,
    event: Event,
    Authorize: AuthJWT = Depends(),
    service: BookmarkService = Depends(get_events_service),
):
    logger.info(f"request delete bookmarks {request}")
    Authorize.fresh_jwt_required()
    user_id = Authorize.get_jwt_subject()
    result = await service.find_and_delete(event.movie_id, user_id)
    return HTTPStatus.NO_CONTENT if result else HTTPStatus.NOT_FOUND
