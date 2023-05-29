from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import Depends

from .mongo_service import MongoService
from db.mongodb import get_mongo
from models.events import ReviewPosted



def review_serializer(review) -> dict:
    return {
        'id': str(review["_id"]),
        'text': review["text"],
        'user_id': review["user_id"],
        'movie_id': review["movie_id"],
        'created_at': review["created_at"],
        'likes': review["likes"],
        'dislikes': review["dislikes"]
    }


class ReviewsService(MongoService):
    pass


@lru_cache()
def get_events_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> ReviewsService:
    return ReviewsService("ugc_movies", "reviews", mongo)