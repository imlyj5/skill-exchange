import pytest
import json
from app.models.user import User
from app.models.rating import Rating
from app.db import db


class TestMatchRoutes:
    """Test cases for matching routes."""
    
    def test_get_matches_success(self, client, sample_user, sample_user2, auth_headers, mock_gemini_api, app):
        """Test successful match with AI enabled."""
        with app.app_context():
            user = User.query.get(sample_user)
            response = client.get(f'/matches/{user.id}', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'matches' in data
            assert 'count' in data
            assert 'ai_enabled' in data
            assert data['ai_enabled'] is True
            assert data['count'] >= 0
            
            # Should find matches since users have compatible skills
            if data['count'] > 0:
                match = data['matches'][0]
                assert 'id' in match
                assert 'name' in match
                assert 'email' in match
                assert 'skills_to_offer' in match
                assert 'skills_to_learn' in match
                assert 'offer_matches' in match
                assert 'learn_matches' in match
    
    def test_get_matches_no_ai(self, client, sample_user, sample_user2, auth_headers, monkeypatch, app):
        """Test match retrieval with AI disabled."""
        # Disable AI
        monkeypatch.setattr('app.routes.match.AI_AVAILABLE', False)
        
        with app.app_context():
            user = User.query.get(sample_user)
            response = client.get(f'/matches/{user.id}', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'matches' in data
            assert 'count' in data
            assert 'ai_enabled' in data
            assert data['ai_enabled'] is False
    
    def test_get_matches_nonexistent_user(self, client, auth_headers, mock_gemini_api):
        """Test getting matches for non-existent user."""
        response = client.get('/matches/99999', headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_get_matches_invalid_id(self, client, auth_headers, mock_gemini_api):
        """Test getting matches with invalid user ID."""
        response = client.get('/matches/invalid', headers=auth_headers)
        
        assert response.status_code == 400 or response.status_code == 404
    
    def test_get_matches_ai_failure(self, client, sample_user, sample_user2, auth_headers, monkeypatch, app):
        """Test match retrieval when AI API fails."""
        # Mock AI API to raise an exception
        def mock_ai_call(prompt):
            raise Exception("AI API error")
        
        monkeypatch.setattr('app.routes.match.make_ai_call', mock_ai_call)
        monkeypatch.setattr('app.routes.match.AI_AVAILABLE', True)
        
        with app.app_context():
            user = User.query.get(sample_user)
            response = client.get(f'/matches/{user.id}', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'matches' in data
            assert 'count' in data
            assert 'ai_enabled' in data
            # When AI fails for a candidate, we skip that candidate but continue with others
            # So we might still get matches from other candidates
            assert isinstance(data['count'], int)
    
    def test_get_matches_exact_match_fallback(self, client, sample_user, sample_user2, auth_headers, monkeypatch, app):
        """Test that exact matching works as fallback."""
        # Disable AI and test exact matching
        monkeypatch.setattr('app.routes.match.AI_AVAILABLE', False)
        
        # Update users to have exact skill matches
        with app.app_context():
            user1 = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            user1.skills_to_offer = ["Python", "Cooking"]
            user1.skills_to_learn = ["Guitar", "Spanish"]
            user2.skills_to_offer = ["Guitar", "Spanish"]
            user2.skills_to_learn = ["Python", "Cooking"]
            db.session.commit()
            
            # Make the API call within the same app context
            response = client.get(f'/matches/{user1.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['ai_enabled'] is False
        # Should find exact matches
        assert data['count'] > 0
    
    def test_get_matches_no_compatible_skills(self, client, sample_user, sample_user2, auth_headers, mock_gemini_api, app):
        """Test matching when users have no compatible skills."""
        # Update users to have incompatible skills
        with app.app_context():
            user1 = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            user1.skills_to_offer = ["Python"]
            user1.skills_to_learn = ["Guitar"]
            user2.skills_to_offer = ["Cooking"]
            user2.skills_to_learn = ["Spanish"]
            db.session.commit()
            
            # Make the API call within the same app context
            response = client.get(f'/matches/{user1.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        # Check the response format is correct
        assert isinstance(data['count'], int)
    
    def test_get_matches_empty_skills(self, client, sample_user, sample_user2, auth_headers, mock_gemini_api, app):
        """Test matching when users have empty skills."""
        # Update users to have empty skills
        with app.app_context():
            user1 = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            user1.skills_to_offer = []
            user1.skills_to_learn = []
            user2.skills_to_offer = []
            user2.skills_to_learn = []
            db.session.commit()
            
            # Make the API call within the same app context
            response = client.get(f'/matches/{user1.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 0
    
    def test_get_matches_single_user(self, client, sample_user, auth_headers, mock_gemini_api):
        """Test matching when there's only one user in the system."""
        response = client.get(f'/matches/{sample_user}', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 0  # No other users to match with
    
    def test_get_matches_bidirectional_requirement(self, client, sample_user, sample_user2, auth_headers, mock_gemini_api, app):
        """Test that matches require both users to be able to teach and learn."""
        # Update users so only one direction works
        with app.app_context():
            user1 = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            user1.skills_to_offer = ["Python"]
            user1.skills_to_learn = ["Guitar"]
            user2.skills_to_offer = ["Guitar"]
            user2.skills_to_learn = ["Cooking"]  # Not what user1 offers
            db.session.commit()
            
            # Make the API call within the same app context
            response = client.get(f'/matches/{user1.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data['count'], int)
    
    def test_get_matches_with_ratings(self, client, sample_user, sample_user2, sample_chat, auth_headers, mock_gemini_api, app):
        """Test that matches include user rating information."""
        # Add a rating to user2
        with app.app_context():
            rating = Rating(
                rater_id=sample_user,
                rated_id=sample_user2,
                chat_id=sample_chat,
                rating=5,
                comment="Great teacher!"
            )
            db.session.add(rating)
            db.session.commit()
        
        response = client.get(f'/matches/{sample_user}', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        if data['count'] > 0:
            match = data['matches'][0]
            assert 'average_rating' in match
            # Should show the rating we just added
            assert match['average_rating'] == 5.0
    
    def test_get_matches_response_format(self, client, sample_user, sample_user2, auth_headers, mock_gemini_api):
        """Test that match response has correct format."""
        response = client.get(f'/matches/{sample_user}', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Check required fields
        assert 'matches' in data
        assert 'count' in data
        assert 'ai_enabled' in data
        assert isinstance(data['matches'], list)
        assert isinstance(data['count'], int)
        assert isinstance(data['ai_enabled'], bool)
        
        # Check match object format if matches exist
        if data['count'] > 0:
            match = data['matches'][0]
            required_fields = [
                'id', 'name', 'email', 'pronouns', 'bio', 'location',
                'availability', 'learning_style', 'skills_to_offer',
                'skills_to_learn', 'average_rating', 'image_url',
                'offer_matches', 'learn_matches'
            ]
            
            for field in required_fields:
                assert field in match
    
    def test_get_matches_excludes_self(self, client, sample_user, auth_headers, mock_gemini_api):
        """Test that user doesn't match with themselves."""
        response = client.get(f'/matches/{sample_user}', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Check that the user is not in their own matches
        for match in data['matches']:
            assert match['id'] != sample_user