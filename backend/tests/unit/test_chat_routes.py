import pytest
import json
from app.models.user import User
from app.models.chat import Chat
from app.models.message import Message
from app.db import db


class TestChatRoutes:
    """Test cases for chat routes."""
    
    def test_get_chats_success(self, client, sample_user, sample_chat, auth_headers, app):
        """Test successful chat retrieval."""
        with app.app_context():
            user = User.query.get(sample_user)
            response = client.get(f'/chats/{user.id}', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'chats' in data
            assert len(data['chats']) >= 1
            
            chat = data['chats'][0]
            assert 'id' in chat
            assert 'user1_id' in chat
            assert 'user2_id' in chat
            assert 'user1_name' in chat
            assert 'user2_name' in chat
            assert 'created_at' in chat
            assert 'is_rated_by_current_user' in chat
    
    def test_get_chats_nonexistent_user(self, client, auth_headers):
        """Test getting chats for non-existent user."""
        response = client.get('/chats/99999', headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_get_chats_invalid_id(self, client, auth_headers):
        """Test getting chats with invalid user ID."""
        response = client.get('/chats/invalid', headers=auth_headers)
        
        assert response.status_code == 400 or response.status_code == 404
    
    def test_get_chats_no_chats(self, client, sample_user, auth_headers, app):
        """Test getting chats when user has no chats."""
        # Create a new user with no chats
        with app.app_context():
            new_user = User(
                name="No Chat User",
                email="nochat@gmail.com",
                pronouns="they/them",
                bio="No chats",
                location="Test City",
                availability="Weekends",
                learning_style="Visual",
                skills_to_offer=["Python"],
                skills_to_learn=["Guitar"]
            )
            new_user.set_password("testpassword")
            db.session.add(new_user)
            db.session.commit()
            
            # Login as new user
            login_response = client.post('/auth/login', json={
                'email': new_user.email,
                'password': 'testpassword'
            })
            
            # Get session cookie
            cookies = login_response.headers.getlist('Set-Cookie')
            headers = {}
            for cookie in cookies:
                if 'session=' in cookie:
                    headers['Cookie'] = cookie.split(';')[0]
                    break
        
        response = client.get(f'/chats/{new_user.id}', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['chats'] == []
    
    def test_create_chat_success(self, client, sample_user, sample_user2, auth_headers, app):
        """Test successful chat creation."""
        with app.app_context():
            user1 = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            response = client.post('/chats', json={
                'user1_id': user1.id,
                'user2_id': user2.id
            }, headers=auth_headers)
            
            assert response.status_code == 201
            data = json.loads(response.data)
            assert 'id' in data
            assert data['user1_id'] == user1.id
            assert data['user2_id'] == user2.id
            assert data['user1_name'] == user1.name
            assert data['user2_name'] == user2.name
            assert 'created_at' in data
    
    def test_create_chat_duplicate(self, client, sample_user, sample_user2, sample_chat, auth_headers, app):
        """Test creating duplicate chat."""
        with app.app_context():
            user1 = User.query.get(sample_user)
            user2 = User.query.get(sample_user2)
            response = client.post('/chats', json={
                'user1_id': user1.id,
                'user2_id': user2.id
            }, headers=auth_headers)
            
            # Duplicate chat returns existing chat with 200 status
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'id' in data
    
    def test_create_chat_nonexistent_users(self, client, sample_user, auth_headers):
        """Test creating chat with non-existent user."""
        response = client.post('/chats', json={
            'user1_id': sample_user,
            'user2_id': 99999
        }, headers=auth_headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_chat_missing_fields(self, client, auth_headers):
        """Test creating chat with missing fields."""
        response = client.post('/chats', json={
            'user1_id': 1
            # Missing user2_id
        }, headers=auth_headers)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_messages_success(self, client, sample_user, sample_chat, sample_message, auth_headers, app):
        """Test successful message retrieval."""
        with app.app_context():
            chat = Chat.query.get(sample_chat)
            response = client.get(f'/chats/{chat.id}/messages', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'messages' in data
            assert len(data['messages']) >= 1
            
            message = data['messages'][0]
            assert 'id' in message
            assert 'chat_id' in message
            assert 'sender_id' in message
            assert 'sender_name' in message
            assert 'content' in message
            assert 'is_read' in message
            assert 'timestamp' in message
    
    def test_get_messages_nonexistent_chat(self, client, sample_user, auth_headers):
        """Test getting messages for non-existent chat."""
        response = client.get('/chats/99999/messages', headers=auth_headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data or 'message' in data
    
    def test_get_messages_invalid_chat_id(self, client, sample_user, auth_headers):
        """Test getting messages with invalid chat ID."""
        response = client.get('/chats/invalid/messages', headers=auth_headers)
        
        assert response.status_code == 400 or response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data or 'message' in data
    
    def test_send_message_success(self, client, sample_user, sample_chat, auth_headers, app):
        """Test successful message sending."""
        with app.app_context():
            user = User.query.get(sample_user)
            chat = Chat.query.get(sample_chat)
            response = client.post(f'/chats/{chat.id}/messages', json={
                'sender_id': user.id,
                'content': 'Test message'
            }, headers=auth_headers)
            
            assert response.status_code == 201
            data = json.loads(response.data)
            assert 'id' in data
            assert data['chat_id'] == chat.id
            assert data['sender_id'] == user.id
            assert data['content'] == 'Test message'
            assert 'timestamp' in data
    
    def test_send_message_nonexistent_chat(self, client, sample_user, auth_headers):
        """Test sending message to non-existent chat."""
        response = client.post('/chats/99999/messages', json={
            'sender_id': sample_user,
            'content': 'Test message'
        }, headers=auth_headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data or 'message' in data
    
    def test_send_message_invalid_chat_id(self, client, sample_user, auth_headers):
        """Test sending message with invalid chat ID."""
        response = client.post('/chats/invalid/messages', json={
            'sender_id': sample_user,
            'content': 'Test message'
        }, headers=auth_headers)
        
        assert response.status_code == 400 or response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data or 'message' in data
    
    def test_send_message_missing_fields(self, client, sample_chat, auth_headers):
        """Test sending message with missing fields."""
        response = client.post(f'/chats/{sample_chat}/messages', json={
            'sender_id': 1
            # Missing content
        }, headers=auth_headers)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_send_message_empty_content(self, client, sample_user, sample_chat, auth_headers):
        """Test sending message with empty content."""
        response = client.post(f'/chats/{sample_chat}/messages', json={
            'sender_id': sample_user,
            'content': ''
        }, headers=auth_headers)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_mark_messages_read_success(self, client, sample_user, sample_chat, sample_message, auth_headers):
        """Test successful message read marking."""
        response = client.put(f'/chats/{sample_chat}/messages/read', json={
            'user_id': sample_user
        }, headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
    
    def test_mark_messages_read_nonexistent_chat(self, client, sample_user, auth_headers):
        """Test marking messages read for non-existent chat."""
        response = client.put('/chats/99999/messages/read', json={
            'user_id': sample_user
        }, headers=auth_headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data or 'message' in data
    
    def test_mark_messages_read_invalid_chat_id(self, client, sample_user, auth_headers):
        """Test marking messages read with invalid chat ID."""
        response = client.put('/chats/invalid/messages/read', json={
            'user_id': sample_user
        }, headers=auth_headers)
        
        assert response.status_code == 400 or response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data or 'message' in data
    
    def test_mark_messages_read_missing_user_id(self, client, sample_chat, auth_headers):
        """Test marking messages read with missing user ID."""
        response = client.put(f'/chats/{sample_chat}/messages/read', json={}, headers=auth_headers)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data