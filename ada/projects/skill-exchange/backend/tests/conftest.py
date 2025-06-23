import pytest
import tempfile
import os
from flask import Flask
from app import create_app
from app.db import db
from app.models.user import User
from app.models.chat import Chat
from app.models.message import Message
from app.models.rating import Rating
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })

    # Create the database and load test data
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    with app.app_context():
        user = User(
            name="Test User",
            email="test@gmail.com",
            pronouns="they/them",
            bio="Test bio",
            location="Test City",
            availability="Weekends",
            learning_style="Visual",
            skills_to_offer=["Python", "Cooking"],
            skills_to_learn=["Guitar", "Spanish"]
        )
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def sample_user2(app):
    """Create a second sample user for testing."""
    with app.app_context():
        user = User(
            name="Test User 2",
            email="test2@gmail.com",
            pronouns="she/her",
            bio="Test bio 2",
            location="Test City 2",
            availability="Weekdays",
            learning_style="Hands-on",
            skills_to_offer=["Guitar", "Spanish"],
            skills_to_learn=["Python", "Cooking"]
        )
        user.set_password("testpassword2")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def sample_chat(app, sample_user, sample_user2):
    """Create a sample chat between two users."""
    with app.app_context():
        chat = Chat(
            user1_id=sample_user,
            user2_id=sample_user2
        )
        db.session.add(chat)
        db.session.commit()
        return chat.id


@pytest.fixture
def sample_message(app, sample_chat, sample_user):
    """Create a sample message in a chat."""
    with app.app_context():
        message = Message(
            chat_id=sample_chat,
            sender_id=sample_user,
            content="Hello, this is a test message!"
        )
        db.session.add(message)
        db.session.commit()
        return message.id


@pytest.fixture
def sample_rating(app, sample_user, sample_user2, sample_chat):
    """Create a sample rating."""
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
        return rating.id


@pytest.fixture
def auth_headers(client, sample_user, app):
    """Get authentication headers for a logged-in user."""
    with app.app_context():
        user = User.query.get(sample_user)
        response = client.post('/auth/login', json={
            'email': user.email,
            'password': 'testpassword'
        })
        cookies = response.headers.getlist('Set-Cookie')
        headers = {}
        for cookie in cookies:
            if 'session=' in cookie:
                headers['Cookie'] = cookie.split(';')[0]
                break
        return headers


@pytest.fixture
def mock_gemini_api(monkeypatch):
    """Mock the Gemini API for testing."""
    class MockGeminiResponse:
        def __init__(self, text="YES"):
            self.text = text
    
    class MockGeminiModel:
        def generate_content(self, prompt):
            return MockGeminiResponse()
    
    class MockGemini:
        def __init__(self):
            self.configured = False
        
        def configure(self, api_key):
            self.configured = True
        
        def GenerativeModel(self, model_name):
            return MockGeminiModel()
    
    mock_genai = MockGemini()
    monkeypatch.setattr('app.routes.match.genai', mock_genai)
    monkeypatch.setattr('app.routes.match.AI_AVAILABLE', True)
    return mock_genai 