from functools import lru_cache

from core.config import settings
from db.mongodb import get_mongo
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from .mongo_service import MongoService


class UserLikeService(MongoService):
    pass


@lru_cache()
def get_events_service(
    mongo: AsyncIOMotorClient = Depends(get_mongo),
) -> UserLikeService:
    return UserLikeService(settings.mongo_dbname, "likes", mongo)
