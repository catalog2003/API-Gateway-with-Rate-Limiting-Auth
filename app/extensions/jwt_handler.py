import jwt
from datetime import datetime, timedelta
from flask import current_app


def create_access_token(user:dict) -> str:
    payload = {
        "user_id" : str(user["_id"]),
        "email" : user["email"],
        "role" : user["role"],
        "type" : "access",
        "exp" : datetime.utcnow() + timedelta(minutes=15)

    }
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")

def decode_token(token: str) -> dict:
    return jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
