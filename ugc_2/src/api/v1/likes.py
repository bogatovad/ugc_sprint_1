from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi_jwt_auth import AuthJWT
from models.events import Like, Event
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
    event: Event,
    Authorize: AuthJWT = Depends(),
    service: UserLikeService = Depends(get_events_service),
):
    logger.info(f"request add like {request}")
    Authorize.fresh_jwt_required()
    user_id = Authorize.get_jwt_subject()
    try:
        await service.add_event(Like(user_id=user_id, movie_id=event.movie_id))
    except DocumentExistsException:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)
    return HTTPStatus.CREATED


@router.delete("/likes", description="Убрать лайк")
async def delete_like(
    request: Request,
    event: Event,
    Authorize: AuthJWT = Depends(),
    service: UserLikeService = Depends(get_events_service),
):
    logger.info(f"request delete like {request}")
    Authorize.fresh_jwt_required()
    user_id = Authorize.get_jwt_subject()
    result = await service.find_and_delete(event.movie_id, user_id)
    return HTTPStatus.NO_CONTENT if result else HTTPStatus.NOT_FOUND
