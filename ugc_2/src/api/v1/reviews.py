from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from models.events import Review, ReviewPosted
from services.reviews import ReviewsService, get_events_service, review_serializer

router = APIRouter()


@router.post(
    "/reviews",
    description="Добавить рецензию к фильму.",
)
async def add_review(
    request: Request,
    event: Review,
    service: ReviewsService = Depends(get_events_service),
):
    logger.info(f'request add review {request}')
    new_review = await service.add_event(
        ReviewPosted(**event.dict(), created_at=datetime.now())
    )
    review = review_serializer(new_review)
    return review


@router.put("/reviews/{review_id}", description="Обновить рецензию")
async def update_review(
    request: Request,
    review_id: str,
    event: Review,
    service: ReviewsService = Depends(get_events_service),
):
    logger.info(f'request update review {request}')
    updated_review = await service.update(review_id, event)
    review = review_serializer(updated_review)
    return review


@router.delete("/reviews/{review_id}", description="Удалить рецензию")
async def delete_review(
    request: Request,
    review_id: str,
    service: ReviewsService = Depends(get_events_service),
):
    logger.info(f'request delete review {request}')
    result = await service.delete(review_id)
    return HTTPStatus.NO_CONTENT if result else HTTPStatus.NOT_FOUND
