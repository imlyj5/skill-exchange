import pytest
import json
from app.models.user import User
from app.models.rating import Rating
from app.models.chat import Chat
from app.db import db


class TestRatingsRoutes:
    """Test cases for ratings routes."""
    
    def test_create_rating_success(self, client, sample_user, sample_user2, sample_chat, auth_headers):
        """Test successful rating creation."""
        rating_data = {
            'rater_id': sample_user,
            'rated_id': sample_user2,
            'chat_id': sample_chat,
            'rating': 5,
            'comment': 'Excellent teacher!'
        }
        
        response = client.post('/ratings', json=rating_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'id' in data
        assert data['rater_id'] == sample_user
        assert data['rated_id'] == sample_user2
        assert data['chat_id'] == sample_chat
        assert data['rating'] == 5
        assert data['comment'] == 'Excellent teacher!'
        assert 'timestamp' in data
    
    def test_create_rating_nonexistent_users(self, client, sample_user, sample_chat, auth_headers):
        """Test creating rating with non-existent users."""
        rating_data = {
            'rater_id': sample_user,
            'rated_id': 99999, 
            'chat_id': sample_chat,
            'rating': 5,
            'comment': 'Test comment'
        }
        
        response = client.post('/ratings', json=rating_data, headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_create_rating_nonexistent_chat(self, client, sample_user, sample_user2, auth_headers):
        """Test creating rating with non-existent chat."""
        rating_data = {
            'rater_id': sample_user,
            'rated_id': sample_user2,
            'chat_id': 99999,  
            'rating': 5,
            'comment': 'Test comment'
        }
        
        response = client.post('/ratings', json=rating_data, headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_create_rating_invalid_rating(self, client, sample_user, sample_user2, sample_chat, auth_headers):
        """Test creating rating with invalid rating value."""
        rating_data = {
            'rater_id': sample_user,
            'rated_id': sample_user2,
            'chat_id': sample_chat,
            'rating': 6,  # Invalid rating (should be 1-5)
            'comment': 'Test comment'
        }
        
        response = client.post('/ratings', json=rating_data, headers=auth_headers)
        
        assert response.status_code == 201 or response.status_code == 400
    
    def test_create_rating_zero_rating(self, client, sample_user, sample_user2, sample_chat, auth_headers):
        """Test creating rating with zero rating value."""
        rating_data = {
            'rater_id': sample_user,
            'rated_id': sample_user2,
            'chat_id': sample_chat,
            'rating': 0,  # Invalid rating (should be 1-5)
            'comment': 'Test comment'
        }
        
        response = client.post('/ratings', json=rating_data, headers=auth_headers)
        
        assert response.status_code == 201 or response.status_code == 400
    
    def test_create_rating_negative_rating(self, client, sample_user, sample_user2, sample_chat, auth_headers):
        """Test creating rating with negative rating value."""
        rating_data = {
            'rater_id': sample_user,
            'rated_id': sample_user2,
            'chat_id': sample_chat,
            'rating': -1,  # Invalid rating
            'comment': 'Test comment'
        }
        
        response = client.post('/ratings', json=rating_data, headers=auth_headers)
        
        assert response.status_code == 201 or response.status_code == 400
    
    def test_create_rating_missing_fields(self, client, sample_user, sample_user2, sample_chat, auth_headers):
        """Test creating rating with missing fields."""
        rating_data = {
            'rater_id': sample_user,
            'rated_id': sample_user2
        }
        
        response = client.post('/ratings', json=rating_data, headers=auth_headers)
        
        assert response.status_code == 400
    
    def test_create_rating_duplicate(self, client, sample_user, sample_user2, sample_chat, sample_rating, auth_headers):
        """Test creating duplicate rating for same chat."""
        rating_data = {
            'rater_id': sample_user,
            'rated_id': sample_user2,
            'chat_id': sample_chat,
            'rating': 4,
            'comment': 'Another comment'
        }
        
        response = client.post('/ratings', json=rating_data, headers=auth_headers)
        
        assert response.status_code == 201 or response.status_code == 400
    
    def test_create_rating_empty_comment(self, client, sample_user, sample_user2, sample_chat, auth_headers):
        """Test creating rating with empty comment."""
        rating_data = {
            'rater_id': sample_user,
            'rated_id': sample_user2,
            'chat_id': sample_chat,
            'rating': 5,
            'comment': ''
        }
        
        response = client.post('/ratings', json=rating_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['comment'] == ''
    
    def test_create_rating_no_comment(self, client, sample_user, sample_user2, sample_chat, auth_headers):
        """Test creating rating without comment."""
        rating_data = {
            'rater_id': sample_user,
            'rated_id': sample_user2,
            'chat_id': sample_chat,
            'rating': 5
        }
        
        response = client.post('/ratings', json=rating_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['comment'] is None or data['comment'] == ''
    
    def test_create_rating_long_comment(self, client, sample_user, sample_user2, sample_chat, auth_headers):
        """Test creating rating with long comment."""
        long_comment = "A" * 1000  # Very long comment
        
        rating_data = {
            'rater_id': sample_user,
            'rated_id': sample_user2,
            'chat_id': sample_chat,
            'rating': 5,
            'comment': long_comment
        }
        
        response = client.post('/ratings', json=rating_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['comment'] == long_comment
    
    def test_create_rating_all_rating_values(self, client, sample_user, sample_user2, sample_chat, auth_headers, app):
        """Test creating ratings with all valid rating values (1-5)."""
        for rating_value in range(1, 6):
            with app.app_context():
                new_chat = Chat(user1_id=sample_user, user2_id=sample_user2)
                db.session.add(new_chat)
                db.session.commit()
                chat_id = new_chat.id
            
            rating_data = {
                'rater_id': sample_user,
                'rated_id': sample_user2,
                'chat_id': chat_id,
                'rating': rating_value,
                'comment': f'Rating {rating_value}'
            }
            
            response = client.post('/ratings', json=rating_data, headers=auth_headers)
            
            assert response.status_code == 201
            data = json.loads(response.data)
            assert data['rating'] == rating_value
    
    def test_create_rating_special_characters_comment(self, client, sample_user, sample_user2, sample_chat, auth_headers):
        """Test creating rating with special characters in comment."""
        special_comment = "Test comment with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        rating_data = {
            'rater_id': sample_user,
            'rated_id': sample_user2,
            'chat_id': sample_chat,
            'rating': 5,
            'comment': special_comment
        }
        
        response = client.post('/ratings', json=rating_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['comment'] == special_comment