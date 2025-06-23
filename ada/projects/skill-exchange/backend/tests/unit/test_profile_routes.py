import pytest
import json
from app.models.user import User
from app.models.rating import Rating
from app.db import db


class TestProfileRoutes:
    """Test cases for profile routes."""
    
    def test_get_profile_success(self, client, sample_user):
        """Test getting a user profile successfully."""
        user = User.query.get(sample_user)
        response = client.get(f'/profile/{sample_user}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == user.id
        assert data['name'] == user.name
        assert data['email'] == user.email
        assert data['pronouns'] == user.pronouns
        assert data['bio'] == user.bio
        assert data['location'] == user.location
        assert data['availability'] == user.availability
        assert data['learning_style'] == user.learning_style
        assert data['skills_to_offer'] == user.skills_to_offer
        assert data['skills_to_learn'] == user.skills_to_learn
        assert 'average_rating' in data
        assert 'image_url' in data
    
    def test_get_profile_nonexistent_user(self, client):
        """Test getting profile for non-existent user."""
        response = client.get('/profile/999')
        assert response.status_code == 404
    
    def test_get_profile_invalid_id(self, client):
        """Test getting profile with invalid ID."""
        response = client.get('/profile/invalid')
        assert response.status_code == 400
    
    def test_update_profile_success(self, client, sample_user, auth_headers, app):
        """Test successful profile update."""
        update_data = {
            'bio': 'Updated bio',
            'location': 'Updated City',
            'availability': 'Weekdays',
            'learning_style': 'Hands-on',
            'skills_to_offer': ['Python', 'JavaScript', 'Cooking'],
            'skills_to_learn': ['Guitar', 'Spanish', 'Yoga']
        }
        
        response = client.put(f'/profile/{sample_user}', 
                            json=update_data, 
                            headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['bio'] == 'Updated bio'
        assert data['location'] == 'Updated City'
        assert data['availability'] == 'Weekdays'
        assert data['learning_style'] == 'Hands-on'
        assert data['skills_to_offer'] == ['Python', 'JavaScript', 'Cooking']
        assert data['skills_to_learn'] == ['Guitar', 'Spanish', 'Yoga']
        
        # Verify the update in database
        with app.app_context():
            user = User.query.get(sample_user)
            assert user.bio == 'Updated bio'
            assert user.location == 'Updated City'
            assert user.availability == 'Weekdays'
            assert user.learning_style == 'Hands-on'
            assert user.skills_to_offer == ['Python', 'JavaScript', 'Cooking']
            assert user.skills_to_learn == ['Guitar', 'Spanish', 'Yoga']
    
    def test_update_profile_partial(self, client, sample_user, auth_headers, app):
        """Test partial profile update."""
        update_data = {
            'bio': 'Only updating bio'
        }
        
        response = client.put(f'/profile/{sample_user}', 
                            json=update_data, 
                            headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['bio'] == 'Only updating bio'
        
        # Verify only bio was updated
        with app.app_context():
            user = User.query.get(sample_user)
            assert user.bio == 'Only updating bio'
            # Other fields should remain unchanged
            assert user.location == 'Test City'
            assert user.availability == 'Weekends'
    
    def test_update_profile_nonexistent_user(self, client, auth_headers):
        """Test updating profile for non-existent user."""
        update_data = {'bio': 'Updated bio'}
        
        response = client.put('/profile/999', 
                            json=update_data, 
                            headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_update_profile_invalid_id(self, client, auth_headers):
        """Test updating profile with invalid ID."""
        update_data = {'bio': 'Updated bio'}
        
        response = client.put('/profile/invalid', 
                            json=update_data, 
                            headers=auth_headers)
        
        assert response.status_code == 400
    
    def test_update_profile_invalid_data(self, client, sample_user, auth_headers):
        """Test updating profile with invalid data."""
        update_data = {'invalid_field': 'value'}
        
        response = client.put(f'/profile/{sample_user}', 
                            json=update_data, 
                            headers=auth_headers)
        
        assert response.status_code == 200  # Invalid fields are ignored
    
    def test_update_profile_empty_skills(self, client, sample_user, auth_headers, app):
        """Test updating profile with empty skills arrays."""
        update_data = {
            'skills_to_offer': [],
            'skills_to_learn': []
        }
        
        response = client.put(f'/profile/{sample_user}', 
                            json=update_data, 
                            headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['skills_to_offer'] == []
        assert data['skills_to_learn'] == []
    
    def test_update_profile_null_values(self, client, sample_user, auth_headers, app):
        """Test updating profile with null values."""
        update_data = {
            'bio': None,
            'location': None,
            'availability': None,
            'learning_style': None
        }
        
        response = client.put(f'/profile/{sample_user}', 
                            json=update_data, 
                            headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['bio'] is None
        assert data['location'] is None
        assert data['availability'] is None
        assert data['learning_style'] is None
    
    def test_get_profile_average_rating(self, client, sample_user, sample_user2, app):
        """Test getting profile with average rating."""
        with app.app_context():
            user = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            # Add some ratings to the user
            from app.models.rating import Rating
            from app.models.chat import Chat
            
            # Create a chat
            chat = Chat(user1_id=user.id, user2_id=user2.id)
            db.session.add(chat)
            db.session.commit()
            
            # Add ratings
            rating1 = Rating(rater_id=user2.id, rated_id=user.id, chat_id=chat.id, rating=4, comment="Good")
            rating2 = Rating(rater_id=user2.id, rated_id=user.id, chat_id=chat.id, rating=5, comment="Excellent")
            db.session.add_all([rating1, rating2])
            db.session.commit()

        response = client.get(f'/profile/{sample_user}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['average_rating'] == 4.5
    
    def test_get_profile_no_ratings(self, client, sample_user):
        """Test getting profile with no ratings."""
        response = client.get(f'/profile/{sample_user}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['average_rating'] == 0.0 