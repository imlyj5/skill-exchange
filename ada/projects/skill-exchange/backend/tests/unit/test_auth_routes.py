import pytest
import json
from app.models.user import User
from app.db import db


class TestAuthRoutes:
    """Test cases for authentication routes."""
    
    def test_signup_success(self, client):
        """Test successful user registration."""
        response = client.post('/auth/signup', json={
            'name': 'Test User',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Test User'
        assert data['email'] == 'test@gmail.com'
        assert 'id' in data
        assert 'message' in data
    
    def test_signup_missing_fields(self, client):
        """Test registration with missing required fields."""
        response = client.post('/auth/signup', json={
            'name': 'Test User'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_signup_duplicate_email(self, client, sample_user, app):
        """Test registration with existing email."""
        with app.app_context():
            user = User.query.get(sample_user)
            response = client.post('/auth/signup', json={
                'name': 'Another User',
                'email': user.email,
                'password': 'testpassword'
            })
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_login_success(self, client, sample_user, app):
        """Test successful user login."""
        with app.app_context():
            user = User.query.get(sample_user)
            response = client.post('/auth/login', json={
                'email': user.email,
                'password': 'testpassword'
            })
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == 'Login successful'
            assert data['user_id'] == user.id
            assert data['name'] == user.name
    
    def test_login_invalid_credentials(self, client, sample_user, app):
        """Test login with wrong password."""
        with app.app_context():
            user = User.query.get(sample_user)
            response = client.post('/auth/login', json={
                'email': user.email,
                'password': 'wrongpassword'
            })
            assert response.status_code == 401
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        response = client.post('/auth/login', json={
            'email': 'nonexistent@gmail.com',
            'password': 'testpassword'
        })
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields."""
        response = client.post('/auth/login', json={
            'email': 'test@gmail.com'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_signup_with_additional_fields(self, client, app):
        """Test registration with optional fields."""
        response = client.post('/auth/signup', json={
            'name': 'Test User',
            'email': 'test@gmail.com',
            'password': 'testpassword',
            'pronouns': 'they/them',
            'bio': 'Test bio',
            'location': 'Test City',
            'availability': 'Weekends',
            'learning_style': 'Visual',
            'skills_to_offer': ['Python', 'Cooking'],
            'skills_to_learn': ['Guitar', 'Spanish']
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Test User'
        assert data['email'] == 'test@gmail.com'
        
        # Verify user was created with additional fields
        with app.app_context():
            user = User.query.filter_by(email='test@gmail.com').first()
            assert user.pronouns == 'they/them'
            assert user.bio == 'Test bio'
            assert user.location == 'Test City'
            assert user.availability == 'Weekends'
            assert user.learning_style == 'Visual'
            assert user.skills_to_offer == ['Python', 'Cooking']
            assert user.skills_to_learn == ['Guitar', 'Spanish'] 