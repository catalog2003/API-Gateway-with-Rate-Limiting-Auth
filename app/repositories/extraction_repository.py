from app.extensions.mongo import get_db
from app.models.extraction_model import extraction_entity

class ExtractionRepository:

    def __init__(self):
        self.collection = get_db().extractions

    def save(self, user_id, url, title, word_count, text):
        doc = extraction_entity(user_id, url, title, word_count, text)
        return self.collection.insert_one(doc)
    
    def get_by_user(self, user_id):
        return list(self.collection.find({"user_id": user_id}))
    