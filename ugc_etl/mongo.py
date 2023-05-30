from config import settings
from pymongo import MongoClient

client = MongoClient()

collections = ("likes", "bookmarks", "reviews")

db_list = ""


def init_mongo(client):
    db = client[settings.mongo_dbname]
    collection = db["new_collection"]
