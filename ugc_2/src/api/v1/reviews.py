from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi_jwt_auth import AuthJWT
from models.events import Review, ReviewPosted
from services.reviews import (ReviewsService, get_events_service,
                              review_serializer)
from core.config import logger
from core.error import DocumentExistsException

from core.config import logger
from fastapi import APIRouter, Depends, Request
from models.events import Review, ReviewPosted
from services.reviews import (ReviewsService, get_events_service,
                              review_serializer)


router = APIRouter()


@router.post(
    "/reviews",
    description="Добавить рецензию к фильму.",
)
async def add_review(
    request: Request,
    event: Review,
    Authorize: AuthJWT = Depends(),
    service: ReviewsService = Depends(get_events_service),
):

    extra = {"tag": "fast_api_app"}
    logger.info(f"request add review {request}", extra=extra)
    Authorize.fresh_jwt_required()
    user_id = Authorize.get_jwt_subject()
    try:
        new_review = await service.add_event(
            ReviewPosted(**event.dict(),
                        created_at=datetime.now(),
                        user_id=user_id)
        )
    except DocumentExistsException:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)
    review = review_serializer(new_review)
    return review


@router.put("/reviews/{review_id}", description="Обновить рецензию")
async def update_review(
    request: Request,
    review_id: str,
    event: Review,
    Authorize: AuthJWT = Depends(),
    service: ReviewsService = Depends(get_events_service),
):
    extra = {"tag": "fast_api_app"}
    logger.info(f"request update review {request}", extra=extra)
    Authorize.fresh_jwt_required()
    user_id = Authorize.get_jwt_subject()
    review = await service.find_one(review_id)
    if not review:
        return HTTPStatus.NOT_FOUND
    if review.get('user_id') != user_id:
        return HTTPStatus.FORBIDDEN
    updated_review = await service.update(review_id, event)
    review = review_serializer(updated_review)
    return review


@router.delete("/reviews/{review_id}", description="Удалить рецензию")
async def delete_review(
    request: Request,
    review_id: str,
    Authorize: AuthJWT = Depends(),
    service: ReviewsService = Depends(get_events_service),
):
    extra = {"tag": "fast_api_app"}
    logger.info(f"request delete review {request}", extra=extra)
    Authorize.fresh_jwt_required()
    user_id = Authorize.get_jwt_subject()
    review = await service.find_one(review_id)
    if not review:
        return HTTPStatus.NOT_FOUND
    if review.get('user_id') != user_id:
        return HTTPStatus.FORBIDDEN
    await service.delete(review_id)
    return HTTPStatus.NO_CONTENT
