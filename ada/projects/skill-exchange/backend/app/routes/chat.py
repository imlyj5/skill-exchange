from flask import Blueprint, request, Response
import sqlalchemy as sa
from ..models.chat import Chat
from ..models.message import Message
from ..models.user import User
from ..models.rating import Rating
from .route_utilities import validate_model, create_model
from ..db import db
import json

chat_bp = Blueprint("chat_bp", __name__, url_prefix="/chats")

@chat_bp.get("/<user_id>")
def get_user_chats(user_id):
    """
    Get all chats this user, including the unread message count
    and a flag indicating if the current user has already rated the chat.
    """
    user = validate_model(User, user_id)
    # Get all chats for the user
    query = db.select(Chat).where((Chat.user1_id == user.id) | (Chat.user2_id == user.id))
    chats = db.session.scalars(query).all()

    # Create a list to store the chat data
    chat_list = []
    for chat in chats:
        # Use to_dict method to get chat data
        chat_data = chat.to_dict(current_user_id=user.id)
        
        # Calculate unread messages for this user in this chat
        unread_count_query = db.select(db.func.count(Message.id)).where(
            Message.chat_id == chat.id,
            Message.sender_id != user.id,
            Message.is_read == False
        )
        unread_count = db.session.scalar(unread_count_query)
        
        # Add the unread count to the chat data
        chat_data["unread_count"] = unread_count
        
        chat_list.append(chat_data)
        
    return Response(
        json.dumps({"chats": chat_list}),
        status=200,
        mimetype="application/json"
    )

@chat_bp.put("/<chat_id>/messages/read")
def mark_messages_as_read(chat_id):
    """
    Mark all messages in a chat as read for a given user.
    """
    # Validate chat_id is an integer
    try:
        chat_id_int = int(chat_id)
    except ValueError:
        return Response(
            json.dumps({"error": "Invalid chat ID format"}),
            status=400,
            mimetype="application/json"
        )
    
    # Validate that chat exists
    chat = db.session.get(Chat, chat_id_int)
    if not chat:
        return Response(
            json.dumps({"error": f"Chat {chat_id} not found"}),
            status=404,
            mimetype="application/json"
        )
    
    data = request.get_json()
    user_id = data.get("user_id")
    # Check if the user id is provided
    if not user_id:
        return Response(
            json.dumps({"error": "user_id is required"}),
            status=400,
            mimetype="application/json"
        )

    # Find all unread messages in this chat that were not sent by the current user and mark them as read
    statement = (
        sa.update(Message)
        .where(
            Message.chat_id == chat_id_int,
            Message.sender_id != user_id,
            Message.is_read == False
        )
        .values(is_read=True)
    )
    db.session.execute(statement)
    db.session.commit()
    
    return Response(
        json.dumps({"message": "Messages marked as read"}),
        status=200,
        mimetype="application/json"
    )

@chat_bp.post("")
def create_chat():
    data = request.get_json()
    user1_id = data.get("user1_id") # Current user initiating the chat
    user2_id = data.get("user2_id")
    # Check if the user ids are provided
    if not user1_id or not user2_id:
        return Response(
            json.dumps({"error": "user1_id and user2_id required"}),
            status=400,
            mimetype="application/json"
        )
    
    # Validate that both users exist
    user1 = db.session.get(User, user1_id)
    user2 = db.session.get(User, user2_id)
    if not user1 or not user2:
        return Response(
            json.dumps({"error": "One or both users not found"}),
            status=404,
            mimetype="application/json"
        )
    
    # Check if chat already exists
    existing_chat = db.session.scalar(
        db.select(Chat).where(
            ((Chat.user1_id == user1_id) & (Chat.user2_id == user2_id)) |
            ((Chat.user1_id == user2_id) & (Chat.user2_id == user1_id))
        )
    )
    if existing_chat:
        # Pass the current user ID to to_dict
        return Response(
            json.dumps(existing_chat.to_dict(current_user_id=user1_id)),
            status=200,
            mimetype="application/json"
        )

    # Create new chat if it doesn't exist
    response_data, status_code = create_model(Chat, data)
    # Add the current_user_id for the to_dict method
    chat = Chat.query.get(response_data["id"])
    return Response(
        json.dumps(chat.to_dict(current_user_id=user1_id)),
        status=status_code,
        mimetype="application/json"
    )

@chat_bp.get("/<chat_id>/messages")
def get_chat_messages(chat_id):
    chat = validate_model(Chat, chat_id)
    # Get all messages for the specific chat, ordered by timestamp
    query = db.select(Message).where(Message.chat_id == chat.id).order_by(Message.timestamp)
    messages = db.session.scalars(query)
    return Response(
        json.dumps({"messages": [msg.to_dict() for msg in messages]}), #Convert the messages to a list of dictionaries
        status=200,
        mimetype="application/json"
    )

@chat_bp.post("/<chat_id>/messages")
def send_message(chat_id):
    chat = validate_model(Chat, chat_id)
    data = request.get_json()
    sender_id = data.get("sender_id")
    content = data.get("content")
    # Check if the sender id and content are provided
    if not sender_id or not content:
        return Response(
            json.dumps({"error": "sender_id and content required"}),
            status=400,
            mimetype="application/json"
        )
    
    # Validate that sender exists
    sender = db.session.get(User, sender_id)
    if not sender:
        return Response(
            json.dumps({"error": "Sender not found"}),
            status=404,
            mimetype="application/json"
        )
    
    # Add chat_id to the data
    data["chat_id"] = chat.id
    
    response_data, status_code = create_model(Message, data)
    return Response(
        json.dumps(response_data),
        status=status_code,
        mimetype="application/json"
    )

@chat_bp.delete("/<chat_id>")
def delete_chat(chat_id):
    chat = validate_model(Chat, chat_id)
    db.session.delete(chat)
    db.session.commit()
    return Response(
        json.dumps({"message": "Chat deleted successfully"}),
        status=200,
        mimetype="application/json"
    )
