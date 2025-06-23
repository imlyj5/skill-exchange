from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import ForeignKey
from datetime import datetime, timezone


class Message(db.Model):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Foreign keys column
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    content: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    # Boolean column for read status, use to show unread message counts in frontend
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Relationship attributes
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
    sender: Mapped["User"] = relationship("User", backref="messages_sent")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_read is None:
            self.is_read = False
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)

    def to_dict(self):
        """Convert message to dictionary with sender name"""
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "sender_id": self.sender_id,
            "sender_name": self.sender.name,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "is_read": self.is_read
        }

    @classmethod
    def from_dict(cls, data):
        """Create message from dictionary data"""
        msg = cls()
        msg.chat_id = data["chat_id"]
        msg.sender_id = data["sender_id"]
        msg.content = data["content"]
        msg.timestamp = data.get("timestamp", datetime.now(timezone.utc))
        msg.is_read = data.get("is_read") if "is_read" in data else False
        return msg
