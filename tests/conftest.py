import pytest
from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.extensions import mongo
import mongomock

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["JWT_SECRET"] = "testsecret"

    mongo.mongo_client = mongomock.MongoClient()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()