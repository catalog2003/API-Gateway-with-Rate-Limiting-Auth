from flask import Blueprint, jsonify, g
from app.middleware.auth_middleware import auth_required
from app.middleware.rate_limiter import rate_limit_required
protected_bp = Blueprint("protected", __name__)

@protected_bp.route("/profile", methods=["GET", "POST"])
@auth_required
@rate_limit_required
def profile():
    return jsonify({
        "email": g.user["email"],
        "role": g.user["role"]
    })
