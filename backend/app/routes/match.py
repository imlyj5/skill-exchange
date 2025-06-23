from flask import Blueprint, Response
from werkzeug.exceptions import HTTPException
from ..models.user import User
from .route_utilities import validate_model
from ..db import db
import google.generativeai as genai
import os
import time
from functools import lru_cache
import json
import math

match_bp = Blueprint("match_bp", __name__, url_prefix="/matches")

# First, determine if AI matching is available
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        AI_AVAILABLE = True
    else:
        # If the API key is not valid, set AI_AVAILABLE to False
        AI_AVAILABLE = False
except Exception as e:
    AI_AVAILABLE = False
    print(f"Failed to configure Gemini API: {e}. AI matching will be disabled.")

def make_ai_call(prompt: str) -> str:
    """Make API call with rate limiting and error handling"""
    try:
        time.sleep(0.1)  # Rate limiting
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"API call failed: {e}")
        raise

@lru_cache(maxsize=1000)
def check_skill_compatibility(skill1: str, skill2: str) -> bool:
    """
    Use AI to check if two skills are compatible/related.
    Returns True if skills are compatible for learning/teaching.
    """
    # Check for exact matches first
    if skill1.lower().strip() == skill2.lower().strip():
        return True
    
    prompt = f"""
    Determine if these two skills are relevant for a skill exchange.
    Return "YES" if:
    - They are the same skill
    - One is a specific type of the other (e.g., "classical piano" and "piano")
    - OR they are in the same general category or domain (e.g., "hiking" and "walking" are both outdoor/fitness/foot-based activities)
    Return "NO" if they are unrelated (e.g., "coding" and "swimming").
    Skill 1: {skill1}
    Skill 2: {skill2}
    Return only "YES" or "NO".
    """
    
    try:
        result = make_ai_call(prompt).upper()
        return result == "YES"
    except Exception as e:
        print(f"Error checking skill compatibility: {e}")
        return skill1.lower() == skill2.lower()  # Fallback to exact match

def find_ai_matches(user_skills_to_offer: list, user_skills_to_learn: list, 
                   candidate_skills_to_offer: list, candidate_skills_to_learn: list):
    """
    Use AI to find matches between user and candidate skills.
    Returns (is_match, offer_matches, learn_matches)
    """
    offer_matches = []
    learn_matches = []
    
    # Check if candidate wants to learn what user offers
    for user_skill in user_skills_to_offer:
        for candidate_skill in candidate_skills_to_learn:
            if check_skill_compatibility(user_skill, candidate_skill):
                offer_matches.append(f"{user_skill} matches {candidate_skill}")
    
    # Check if user wants to learn what candidate offers
    for user_skill in user_skills_to_learn:
        for candidate_skill in candidate_skills_to_offer:
            if check_skill_compatibility(user_skill, candidate_skill):
                learn_matches.append(f"{candidate_skill} matches {user_skill}")
    
    # If both offer_matches and learn_matches exist, return True
    is_match = len(offer_matches) > 0 and len(learn_matches) > 0
    return is_match, offer_matches, learn_matches

@match_bp.get("/<user_id>")
def get_matches(user_id):
    try:
        user = validate_model(User, user_id)
        user_dict = user.to_dict()
        query = db.select(User).where(User.id != user.id)  # Get all candidates except the input user
        candidates = db.session.scalars(query)
        matches = []
        
        for candidate in candidates:
            candidate_dict = candidate.to_dict()
            user_offer = set(user.skills_to_offer or [])
            user_learn = set(user.skills_to_learn or [])
            candidate_offer = set(candidate.skills_to_offer or [])
            candidate_learn = set(candidate.skills_to_learn or [])
            
            # If AI is enabled, use AI matching (which includes exact matches)
            if AI_AVAILABLE:
                try:
                    is_match, offer_matches, learn_matches = find_ai_matches(
                        list(user_offer), list(user_learn),
                        list(candidate_offer), list(candidate_learn)
                    )
                    # If AI found matches, use them
                    if is_match:
                        candidate_dict["offer_matches"] = offer_matches
                        candidate_dict["learn_matches"] = learn_matches
                        matches.append(candidate_dict)
                except Exception as e:
                    print(f"Error in AI matching for candidate {candidate.id}: {e}")  # AI failed, no match for this candidate
                    
            # If AI is disabled, use exact matching only
            else:
                offer_match = user_offer & candidate_learn
                learn_match = user_learn & candidate_offer
                
                if offer_match and learn_match:
                    candidate_dict["offer_matches"] = list(offer_match)
                    candidate_dict["learn_matches"] = list(learn_match)
                    matches.append(candidate_dict)
        
        response_data = {
            "matches": matches,
            "count": len(matches),
            "ai_enabled": AI_AVAILABLE
        }
        return Response(
            json.dumps(response_data),
            status=200,
            mimetype="application/json"
        )
    except HTTPException:
        # Re-raise HTTPExceptions from validate_model
        raise
    except Exception as e:  # If there is an error, return an empty list
        print(f"Error in get_matches: {e}")
        return Response(
            json.dumps({"matches": [], "count": 0, "ai_enabled": AI_AVAILABLE}),
            status=200,
            mimetype="application/json"
        )
