from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import Depends

from .mongo_service import MongoService
from db.mongodb import get_mongo


class UserLikeService(MongoService):
    pass


@lru_cache()
def get_events_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> UserLikeService:
    return UserLikeService("ugc_movies", "likes", mongo)