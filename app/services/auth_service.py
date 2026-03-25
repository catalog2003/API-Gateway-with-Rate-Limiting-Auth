from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password
from app.extensions.jwt_handler import create_access_token

class AuthService:

    def __init__(self):
        self.user_repo = UserRepository()
    
    def register(self, email:str ,password: str, role: str = "free"):
        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("User already exists")
        
        password_hash = hash_password(password)
        self.user_repo.create_user(email, password_hash)

        return {"meassage": "User registered successfully"}
    
    def login(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise ValueError("Invalid credentials")
        
        if not verify_password(password, user["password_hash"]):
            raise ValueError("Invalid credentials")
        
        token = create_access_token(user)
        return {"access_token": token}
    
    
    