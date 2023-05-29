from http import HTTPStatus

from fastapi import APIRouter, Depends, Request

from models.events import Like
from services.likes import UserLikeService, get_events_service


router = APIRouter()


@router.post(
    "/likes",
    description="Поставить лайк фильму.",
)
async def add_like(
    request: Request, event: Like, service: UserLikeService = Depends(get_events_service)
):
    await service.add_event(event)
    return HTTPStatus.CREATED


@router.delete(
    "/likes",
    description="Убрать лайк"
)
async def delete_like(
    request: Request, event: Like, service: UserLikeService = Depends(get_events_service)
):
    result = await service.find_and_delete(event)
    return  HTTPStatus.NO_CONTENT if result else HTTPStatus.NOT_FOUND

    