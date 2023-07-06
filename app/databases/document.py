import motor.motor_asyncio

from app.settings import get_mongodb_settings

mongodb_settings = get_mongodb_settings()
mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_settings.mongo_db_url)
#document_db = mongodb_client[mongodb_settings.mongo_db_name]


def get_document_db():
    return mongodb_client[mongodb_settings.mongo_db_name]