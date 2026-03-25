from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from app.schemas.extraction_schema import ExtractionRequestSchema
from app.services.extraction_service import ExtractionService
from app.middleware.auth_middleware import auth_required
from app.middleware.rate_limiter import rate_limit_required

extraction_bp = Blueprint("extraction", __name__)
service = None

@extraction_bp.route("/extract", methods=["POST"])
@auth_required
@rate_limit_required
def extract():
    global service
    if service is None:
        service = ExtractionService()

    try:
        data = ExtractionRequestSchema(**request.json)

        result = service.extract_text(
            user_id=str(g.user["_id"]),
            url=str(data.url)
        )

        return jsonify(result)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400