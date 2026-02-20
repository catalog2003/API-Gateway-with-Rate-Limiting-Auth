from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from app.services.auth_service import AuthService


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    try: 
        auth_service = AuthService()
        data = RegisterSchema(**request.json)
        result = auth_service.register(data.email, data.password, data.role)
        return jsonify(result), 201
    
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        auth_service = AuthService()
        data = LoginSchema(**request.json)
        result = auth_service.login(data.email, data.password)
        return jsonify(result)
    
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 401