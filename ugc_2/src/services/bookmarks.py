from functools import lru_cache

from core.config import settings
from db.mongodb import get_mongo
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from .mongo_service import MongoService


class BookmarkService(MongoService):
    pass


@lru_cache()
def get_events_service(
    mongo: AsyncIOMotorClient = Depends(get_mongo),
) -> BookmarkService:
    return BookmarkService(settings.mongo_dbname, "bookmarks", mongo)
