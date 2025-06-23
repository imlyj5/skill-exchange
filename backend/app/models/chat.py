from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import ForeignKey
from datetime import datetime, timezone

class Chat(db.Model):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Foreign keys column
    user1_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user2_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    # Relationship attributes
    user1: Mapped["User"] = relationship("User", foreign_keys=[user1_id], backref="chats_as_user1")
    user2: Mapped["User"] = relationship("User", foreign_keys=[user2_id], backref="chats_as_user2")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)

    def to_dict(self, current_user_id=None):
        """Convert chat to dictionary with relationship data"""
        result = {
            "id": self.id,
            "user1_id": self.user1_id,
            "user2_id": self.user2_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user1_name": self.user1.name,
            "user2_name": self.user2.name,
            "user1_avatar": self.user1.image_url,
            "user2_avatar": self.user2.image_url,
        }
        
        if current_user_id is not None:
            # Import Rating here to avoid circular import
            from .rating import Rating
            # Check if the current user has already submitted a rating in this chat
            rating_exists = db.session.query(Rating.id).filter_by(
                chat_id=self.id,
                rater_id=current_user_id
            ).first() is not None
            # Add the new flag for the frontend
            result["is_rated_by_current_user"] = rating_exists
            
        return result

    @classmethod
    def from_dict(cls, data):
        """Create chat from dictionary data"""
        chat = cls()
        chat.user1_id = data["user1_id"]
        chat.user2_id = data["user2_id"]
        chat.created_at = data.get("created_at") or datetime.now(timezone.utc)
        return chat