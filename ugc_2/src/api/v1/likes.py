from http import HTTPStatus

from core.config import logger
from core.error import DocumentExistsException
from core.logger import extra
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_jwt_auth import AuthJWT
from models.events import Event, Like
from services.likes import UserLikeService, get_events_service

router = APIRouter()


@router.post(
    "/likes",
    description="Поставить лайк фильму.",
)
async def add_like(
    request: Request,
    event: Event,
    authorize: AuthJWT = Depends(),
    service: UserLikeService = Depends(get_events_service),
):
    logger.info(f"request add like {request}", extra=extra)
    authorize.fresh_jwt_required()
    user_id = authorize.get_jwt_subject()
    logger.info(f"user {user_id} is authorized", extra=extra)
    try:
        await service.add_event(Like(user_id=user_id, movie_id=event.movie_id))
    except DocumentExistsException:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)
    return HTTPStatus.CREATED


@router.delete("/likes", description="Убрать лайк")
async def delete_like(
    request: Request,
    event: Event,
    authorize: AuthJWT = Depends(),
    service: UserLikeService = Depends(get_events_service),
):
    logger.info(f"request delete like {request}", extra=extra)
    authorize.fresh_jwt_required()
    user_id = authorize.get_jwt_subject()
    logger.info(f"user {user_id} is authorized", extra=extra)
    result = await service.find_and_delete(event.movie_id, user_id)
    return HTTPStatus.NO_CONTENT if result else HTTPStatus.NOT_FOUND
