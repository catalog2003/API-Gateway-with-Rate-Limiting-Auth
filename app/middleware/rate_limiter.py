from flask import jsonify, g, make_response
from functools import wraps
from app.services.rate_limiter_service import RateLimiterService
from app.core.logger import logger
from app.extensions.metrics import rate_limit_hits

# instantiate lazily so Redis is initialized by the app factory first
rate_limiter_service = None

def rate_limit_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        user_id = str(g.user["_id"])
        role = g.user.get("role", "free")

        global rate_limiter_service
        if rate_limiter_service is None:
            rate_limiter_service = RateLimiterService()

        allowed, remaining, capacity = rate_limiter_service.allow_request(user_id, role)
        
        if not allowed:
               logger.warning(f"Rate limit exceeded for user {user_id}")
               rate_limit_hits.inc()

               response = jsonify({"error": "Rate limit exceeded"})
               response.status_code = 429
               response.headers["X-RateLimit-Limit"] = str(capacity)
               response.headers["X-RateLimit-Remaining"] = str(remaining)

               return response
        response = f(*args, **kwargs)
        
        response = make_response(response)

        response.headers["X-RateLimit-Limit"] = str(capacity)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response
    return wrapper