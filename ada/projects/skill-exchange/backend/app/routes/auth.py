from flask import Blueprint, request, Response
from ..models.user import User
from ..db import db
from .route_utilities import create_model
import json

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@auth_bp.post("/signup")
def signup():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password") or not data.get("name"):
        return Response(
            json.dumps({"error": "Missing required fields"}),
            status=400,
            mimetype="application/json"
        )

    # Check if the email is already registered
    if User.query.filter_by(email=data["email"]).first():
        return Response(
            json.dumps({"error": "Email already registered"}),
            status=400,
            mimetype="application/json"
        )

    # Create the user
    response_data, status_code = create_model(
        User, 
        data, 
        additional_fields={"message": "User created successfully"}
    )
    return Response(
        json.dumps(response_data),
        status=status_code,
        mimetype="application/json"
    )

@auth_bp.post("/login")
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return Response(
            json.dumps({"error": "Missing email or password"}),
            status=400,
            mimetype="application/json"
        )

    # Check if the email is registered
    user = User.query.filter_by(email=data["email"]).first()
    # Check if the password is correct
    if user and user.check_password(data["password"]):
        # Return the user id and name
        return Response(
            json.dumps({"message": "Login successful", "user_id": user.id, "name": user.name}),
            status=200,
            mimetype="application/json"
        )
    else:
        return Response(
            json.dumps({"error": "Invalid credentials"}),
            status=401,
            mimetype="application/json"
        )
