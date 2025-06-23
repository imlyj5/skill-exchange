from flask import Blueprint, request, jsonify
from ..models.rating import Rating
from ..models.user import User
from ..models.chat import Chat
from .route_utilities import validate_model, create_model
from ..db import db

rating_bp = Blueprint("rating_bp", __name__, url_prefix="/ratings")

@rating_bp.post("")
def create_rating():
    """
    Creates a new rating for a user within a specific chat.
    """
    data = request.get_json()
    
    # Data Validation
    rater_id = data.get("rater_id")
    rated_id = data.get("rated_id")
    chat_id = data.get("chat_id")
    rating_value = data.get("rating")
    comment = data.get("comment")

    if not all([rater_id, rated_id, chat_id, rating_value]):
        return jsonify({"error": "Missing required fields: rater_id, rated_id, chat_id, and rating are required."}), 400

    # Model Validation
    validate_model(User, rater_id)
    validate_model(User, rated_id)
    validate_model(Chat, chat_id)

    # Create New Rating
    response_data, status_code = create_model(Rating, data)
    return jsonify(response_data), status_code
