from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from db.mongodb import get_mongo


class MongoService:
    """Сервис для сохранения событий в MongoDB"""
    def __init__(self, dbname: str, collection: str, client: AsyncIOMotorClient):
        self.client = client
        self.dbname = dbname
        self.db = self.client[dbname]
        self.collection = self.db.get_collection(collection)

    async def add_event(self, event) -> dict:
        event = await self.collection.insert_one(event.dict())
        new_event = await self.collection.find_one({"_id": event.inserted_id})
        return new_event
    
    async def delete(self, source_id):
        deleted_event = await self.collection.delete_one({"_id": ObjectId(source_id)})
        return deleted_event

    async def find_and_delete(self, event):
        deleted_event = await self.collection.find_one_and_delete(
            {"movie_id": event.movie_id, "user_id": event.user_id}
        )
        return deleted_event 

    