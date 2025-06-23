from flask import Flask, send_from_directory
from .db import db, migrate
import os
from .models import user, chat, message, rating
from .routes.auth import auth_bp
from .routes.profile import profile_bp
from .routes.match import match_bp
from .routes.chat import chat_bp
from .routes.upload import upload_bp
from .routes.ratings import rating_bp
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

def create_app(config=None):
    app = Flask(__name__)
    
    # Configure CORS to allow file uploads and static file serving
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://localhost:3001"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB max file size
    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "..", "uploads")

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(match_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(rating_bp)

    return app