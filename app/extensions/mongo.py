from pymongo import MongoClient
from pymongo.errors import ConfigurationError

mongo_client = None

def init_mongo(app):
    global mongo_client
    mongo_client = MongoClient(app.config["MONGO_URI"])

def get_db():
    if mongo_client is None:
        raise RuntimeError("MongoDB not initialized. Call init_mongo() first.")
    try:
        return mongo_client.get_default_database()
    except ConfigurationError:
        # Fallback for test environments (mongomock) where no default database is set
        return mongo_client.get_database("testdb")
