from app.extensions.mongo import get_db
from app.models.user_model import user_entity
from bson import ObjectId

class UserRepository:

    def __init__(self):
        self.db = get_db()
        self.collection = self.db.users
    
    def create_user(self, email, password_hash, role="free"):
        user = user_entity(email, password_hash, role)
        return self.collection.insert_one(user)
    
    def get_by_email(self, email):
        return self.collection.find_one({"email": email})
    
    def get_by_id(self, user_id):
        return self.collection.find_one({"_id": ObjectId(user_id)})
        