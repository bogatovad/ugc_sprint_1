from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from models import Event
from services.events_service import EventService, get_events_service

router = APIRouter()


@router.post(
    "/view_progress",
    description="Получение данных о времени просмотра фильма.",
)
async def post_view_progress(
    request: Request, event: Event, service: EventService = Depends(get_events_service)
):
    await service.send_event(event)
    return HTTPStatus.CREATED
