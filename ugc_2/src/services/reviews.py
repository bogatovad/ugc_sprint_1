from functools import lru_cache
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import Depends

from .mongo_service import MongoService
from db.mongodb import get_mongo
from core.config import settings



def review_serializer(review) -> dict:
    return {
        'id': str(review["_id"]),
        'text': review["text"],
        'user_id': review["user_id"],
        'movie_id': review["movie_id"],
        'created_at': review["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
        'likes': review["likes"],
        'dislikes': review["dislikes"]
    }


class ReviewsService(MongoService):
    pass


@lru_cache()
def get_events_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> ReviewsService:
    return ReviewsService(settings.mongo_dbname, "reviews", mongo)