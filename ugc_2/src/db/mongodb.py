from motor.motor_asyncio import AsyncIOMotorClient

mongo_client: AsyncIOMotorClient | None = None


async def get_mongo() -> AsyncIOMotorClient | None:
    return mongo_client