from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request

from models.events import Review, ReviewPosted
from services.reviews import ReviewsService, get_events_service, review_serializer


router = APIRouter()


@router.post(
    "/reviews",
    description="Добавить рецензию к фильму.",
)
async def add_review(
    request: Request, event: Review, service: ReviewsService = Depends(get_events_service)
):
    new_review = await service.add_event(ReviewPosted(**event.dict(), created_at=datetime.now()))
    review = review_serializer(new_review)
    return review


@router.delete(
    "/reviews/{review_id}",
    description="Удалить рецензию"
)
async def delete_review(
    request: Request, review_id: str, service: ReviewsService = Depends(get_events_service)
):
    result = await service.delete(review_id)
    if not result:
        return HTTPStatus.NOT_FOUND
    return HTTPStatus.NO_CONTENT