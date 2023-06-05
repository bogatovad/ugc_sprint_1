from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from core.error import DocumentExistsException

class MongoService:
    """Сервис для сохранения событий в MongoDB"""

    def __init__(self, dbname: str, collection: str, client: AsyncIOMotorClient):
        self.client = client
        self.dbname = dbname
        self.db = self.client[dbname]
        self.collection = self.db.get_collection(collection)

    async def find_one(self, source_id):
        db_event = await self.collection.find_one({"_id": ObjectId(source_id)})
        return db_event

    async def add_event(self, event) -> dict:
        res = await self.collection.find_one({"user_id": event.user_id, "movie_id": event.movie_id})
        if res:    
            raise DocumentExistsException
        event = await self.collection.insert_one(event.dict())
        new_event = await self.collection.find_one({"_id": event.inserted_id})
        return new_event

    async def update(self, source_id, event):
        await self.collection.update_one(
            {"_id": ObjectId(source_id)}, {"$set": dict(event)}
        )
        updated_event = await self.collection.find_one({"_id": ObjectId(source_id)})
        return updated_event

    async def delete(self, source_id):
        deleted_event = await self.collection.delete_one({"_id": ObjectId(source_id)})
        return deleted_event

    async def find_and_delete(self, movie_id, user_id):
        deleted_event = await self.collection.find_one_and_delete(
            {"movie_id": movie_id, "user_id": user_id}
        )
        return deleted_event

