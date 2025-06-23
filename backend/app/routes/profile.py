from flask import Blueprint, request, Response
from ..models.user import User
from .route_utilities import validate_model
from ..db import db
import json

profile_bp = Blueprint("profile_bp", __name__, url_prefix="/profile")

@profile_bp.get("/<user_id>")
def get_profile(user_id):
    user = validate_model(User, user_id)
    return Response(
        json.dumps(user.to_dict()),
        status=200,
        mimetype="application/json"
    )

@profile_bp.put("/<user_id>")
def update_profile(user_id):
    user = validate_model(User, user_id)
    data = request.get_json()
    # Update only allowed fields
    for field in [
        "name", "pronouns", "bio", "location", "availability",
        "learning_style", "skills_to_offer", "skills_to_learn", "rating",
        "image_url"
    ]:
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()
    return Response(
        json.dumps(user.to_dict()),
        status=200,
        mimetype="application/json"
    )
