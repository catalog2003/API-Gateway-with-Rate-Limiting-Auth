from functools import wraps
from flask import request, jsonify, g
from app.extensions.jwt_handler import decode_token
from app.repositories.user_repository import UserRepository
import jwt

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing token"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = decode_token(token)
            user_repo = UserRepository()
            user = user_repo.get_by_id(payload["user_id"])

            if not user:
                return jsonify({"error": "User not found"}), 401

            g.user = user

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return wrapper
