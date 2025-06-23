from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import Optional
from sqlalchemy import ForeignKey
from datetime import datetime, timezone

class Rating(db.Model):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rater_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # The user who is being rated
    rated_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # The chat this rating is associated with
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    
    rating: Mapped[int] = mapped_column(nullable=False) 
    comment: Mapped[Optional[str]]
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    # Relationship attributes
    rater: Mapped["User"] = relationship("User", foreign_keys=[rater_id], back_populates="ratings_given")
    rated: Mapped["User"] = relationship("User", foreign_keys=[rated_id], back_populates="ratings_received")
    chat: Mapped["Chat"] = relationship("Chat", backref="ratings")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)

    def to_dict(self):
        """Convert rating to dictionary with rater name"""
        return {
            "id": self.id,
            "rater_id": self.rater_id,
            "rated_id": self.rated_id,
            "chat_id": self.chat_id,
            "rater_name": self.rater.name,
            "rating": self.rating,
            "comment": self.comment,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }

    @classmethod
    def from_dict(cls, data):
        """Create rating from dictionary data"""
        rating = cls()
        rating.rater_id = data["rater_id"]
        rating.rated_id = data["rated_id"]
        rating.chat_id = data["chat_id"]
        rating.rating = data["rating"]
        rating.comment = data.get("comment")
        rating.timestamp = data.get("timestamp") or datetime.now(timezone.utc)
        return rating