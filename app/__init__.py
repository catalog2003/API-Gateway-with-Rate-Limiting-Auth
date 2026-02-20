from flask import Flask
from app.config import Config
from app.routes.auth_routes import auth_bp
from app.routes.protected_routes import protected_bp
from app.routes.extraction_routes import extraction_bp
from app.routes.health_routes import health_bp
from app.extensions.mongo import init_mongo
from app.extensions.redis_client import init_redis


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    

    init_mongo(app)
    init_redis(app)
    

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(protected_bp, url_prefix="/api")
    app.register_blueprint(extraction_bp, url_prefix="/api")
    

    

    return app
