import pytest
from datetime import datetime, timezone
from app.models.user import User
from app.models.chat import Chat
from app.models.message import Message
from app.models.rating import Rating
from werkzeug.security import check_password_hash
from app.db import db


class TestUserModel:
    """Test cases for the User model."""
    
    def test_user_creation(self, app):
        """Test creating a new user."""
        with app.app_context():
            user = User(
                name="John",
                email="john@gmail.com",
                pronouns="he/him",
                bio="Test bio",
                location="Test City",
                availability="Weekends",
                learning_style="Visual",
                skills_to_offer=["Python", "Cooking"],
                skills_to_learn=["Guitar", "Spanish"]
            )
            user.set_password("testpassword")
            
            assert user.name == "John"
            assert user.email == "john@gmail.com"
            assert user.pronouns == "he/him"
            assert user.bio == "Test bio"
            assert user.location == "Test City"
            assert user.availability == "Weekends"
            assert user.learning_style == "Visual"
            assert user.skills_to_offer == ["Python", "Cooking"]
            assert user.skills_to_learn == ["Guitar", "Spanish"]
            assert check_password_hash(user.password_hash, "testpassword")
    
    def test_user_password_check(self, app):
        """Test password checking functionality."""
        with app.app_context():
            user = User(name="Test User", email="test@gmail.com")
            user.set_password("testpassword")
            
            assert user.check_password("testpassword") is True
            assert user.check_password("wrongpassword") is False
    
    def test_user_average_rating_no_ratings(self, app):
        """Test average rating calculation with no ratings."""
        with app.app_context():
            user = User(name="Test User", email="test@gmail.com")
            assert user.average_rating == 0
    
    def test_user_average_rating_with_ratings(self, app, sample_user, sample_user2, sample_chat):
        """Test average rating calculation with ratings."""
        with app.app_context():
            user = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            chat = Chat.query.get(sample_chat)
            rating1 = Rating(
                rater_id=user2.id,
                rated_id=user.id,
                chat_id=chat.id,
                rating=4
            )
            rating2 = Rating(
                rater_id=user2.id,
                rated_id=user.id,
                chat_id=chat.id,
                rating=5
            )
            
            db.session.add(rating1)
            db.session.add(rating2)
            db.session.commit()
            
            db.session.refresh(user)
            assert user.average_rating == 4.5
    
    def test_user_to_dict(self, app):
        """Test user to_dict method."""
        with app.app_context():
            user = User(
                name="Test User",
                email="test@gmail.com",
                pronouns="they/them",
                bio="Test bio",
                location="Test City",
                skills_to_offer=["Python"],
                skills_to_learn=["Guitar"]
            )
            
            user_dict = user.to_dict()
            
            assert user_dict["name"] == "Test User"
            assert user_dict["email"] == "test@gmail.com"
            assert user_dict["pronouns"] == "they/them"
            assert user_dict["bio"] == "Test bio"
            assert user_dict["location"] == "Test City"
            assert user_dict["skills_to_offer"] == ["Python"]
            assert user_dict["skills_to_learn"] == ["Guitar"]
            assert "average_rating" in user_dict
            assert "image_url" in user_dict
    
    def test_user_from_dict(self, app):
        """Test creating user from dictionary."""
        with app.app_context():
            user_data = {
                "name": "Test User",
                "email": "test@gmail.com",
                "pronouns": "they/them",
                "bio": "Test bio",
                "location": "Test City",
                "availability": "Weekends",
                "learning_style": "Visual",
                "skills_to_offer": ["Python"],
                "skills_to_learn": ["Guitar"],
                "password": "testpassword"
            }
            
            user = User.from_dict(user_data)
            
            assert user.name == "Test User"
            assert user.email == "test@gmail.com"
            assert user.pronouns == "they/them"
            assert user.bio == "Test bio"
            assert user.location == "Test City"
            assert user.availability == "Weekends"
            assert user.learning_style == "Visual"
            assert user.skills_to_offer == ["Python"]
            assert user.skills_to_learn == ["Guitar"]
            assert check_password_hash(user.password_hash, "testpassword")


class TestChatModel:
    """Test cases for the Chat model."""
    
    def test_chat_creation(self, app, sample_user, sample_user2):
        """Test creating a new chat."""
        with app.app_context():
            user1 = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            chat = Chat(
                user1_id=user1.id,
                user2_id=user2.id
            )
            
            assert chat.user1_id == user1.id
            assert chat.user2_id == user2.id
            assert isinstance(chat.created_at, datetime)
    
    def test_chat_to_dict(self, app, sample_chat, sample_user, sample_user2):
        """Test chat to_dict method."""
        with app.app_context():
            chat = Chat.query.get(sample_chat)
            user1 = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            chat_dict = chat.to_dict()
            
            assert chat_dict["id"] == chat.id
            assert chat_dict["user1_id"] == user1.id
            assert chat_dict["user2_id"] == user2.id
            assert chat_dict["user1_name"] == user1.name
            assert chat_dict["user2_name"] == user2.name
            assert "created_at" in chat_dict
    
    def test_chat_to_dict_with_current_user(self, app, sample_chat, sample_user, sample_user2):
        """Test chat to_dict method with current user for rating check."""
        with app.app_context():
            chat = Chat.query.get(sample_chat)
            user1 = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            rating = Rating(
                rater_id=user1.id,
                rated_id=user2.id,
                chat_id=chat.id,
                rating=5
            )
            db.session.add(rating)
            db.session.commit()
            
            chat_dict = chat.to_dict(current_user_id=user1.id)
            
            assert chat_dict["is_rated_by_current_user"] is True
    
    def test_chat_from_dict(self, app, sample_user, sample_user2):
        """Test creating chat from dictionary."""
        with app.app_context():
            user1 = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            chat_data = {
                "user1_id": user1.id,
                "user2_id": user2.id
            }
            
            chat = Chat.from_dict(chat_data)
            
            assert chat.user1_id == user1.id
            assert chat.user2_id == user2.id


class TestMessageModel:
    """Test cases for the Message model."""
    
    def test_message_creation(self, app, sample_chat, sample_user):
        """Test creating a new message."""
        with app.app_context():
            chat = Chat.query.get(sample_chat)
            user = User.query.get(sample_user)
            message = Message(
                chat_id=chat.id,
                sender_id=user.id,
                content="Hello, this is a test message!"
            )
            
            assert message.chat_id == chat.id
            assert message.sender_id == user.id
            assert message.content == "Hello, this is a test message!"
            assert message.is_read is False
            assert isinstance(message.timestamp, datetime)
    
    def test_message_to_dict(self, app, sample_message, sample_user):
        """Test message to_dict method."""
        with app.app_context():
            message = Message.query.get(sample_message)
            user = User.query.get(sample_user)
            message_dict = message.to_dict()
            
            assert message_dict["id"] == message.id
            assert message_dict["chat_id"] == message.chat_id
            assert message_dict["sender_id"] == user.id
            assert message_dict["sender_name"] == user.name
            assert message_dict["content"] == "Hello, this is a test message!"
            assert message_dict["is_read"] is False
            assert "timestamp" in message_dict
    
    def test_message_from_dict(self, app, sample_chat, sample_user):
        """Test creating message from dictionary."""
        with app.app_context():
            chat = Chat.query.get(sample_chat)
            user = User.query.get(sample_user)
            message_data = {
                "chat_id": chat.id,
                "sender_id": user.id,
                "content": "Test message from dict"
            }
            
            message = Message.from_dict(message_data)
            
            assert message.chat_id == chat.id
            assert message.sender_id == user.id
            assert message.content == "Test message from dict"


class TestRatingModel:
    """Test cases for the Rating model."""
    
    def test_rating_creation(self, app, sample_user, sample_user2, sample_chat):
        """Test creating a new rating."""
        with app.app_context():
            user1 = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            chat = Chat.query.get(sample_chat)
            rating = Rating(
                rater_id=user1.id,
                rated_id=user2.id,
                chat_id=chat.id,
                rating=5,
                comment="Excellent teacher!"
            )
            
            assert rating.rater_id == user1.id
            assert rating.rated_id == user2.id
            assert rating.chat_id == chat.id
            assert rating.rating == 5
            assert rating.comment == "Excellent teacher!"
            assert isinstance(rating.timestamp, datetime)
    
    def test_rating_to_dict(self, app, sample_rating, sample_user):
        """Test rating to_dict method."""
        with app.app_context():
            rating = Rating.query.get(sample_rating)
            user = User.query.get(sample_user)
            rating_dict = rating.to_dict()
            
            assert rating_dict["id"] == rating.id
            assert rating_dict["rater_id"] == user.id
            assert rating_dict["rater_name"] == user.name
            assert rating_dict["rating"] == 5
            assert rating_dict["comment"] == "Great teacher!"
            assert "timestamp" in rating_dict
    
    def test_rating_from_dict(self, app, sample_user, sample_user2, sample_chat):
        """Test creating rating from dictionary."""
        with app.app_context():
            user1 = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            chat = Chat.query.get(sample_chat)
            rating_data = {
                "rater_id": user1.id,
                "rated_id": user2.id,
                "chat_id": chat.id,
                "rating": 4,
                "comment": "Good experience"
            }
            
            rating = Rating.from_dict(rating_data)
            
            assert rating.rater_id == user1.id
            assert rating.rated_id == user2.id
            assert rating.chat_id == chat.id
            assert rating.rating == 4
            assert rating.comment == "Good experience" 