from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ARRAY

class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    pronouns: Mapped[Optional[str]]
    bio: Mapped[Optional[str]]
    location: Mapped[Optional[str]]
    availability: Mapped[Optional[str]]
    learning_style: Mapped[Optional[str]]
    skills_to_offer: Mapped[Optional[List[str]]] = mapped_column(ARRAY(db.String(50)))
    skills_to_learn: Mapped[Optional[List[str]]] = mapped_column(ARRAY(db.String(50)))
    image_url: Mapped[Optional[str]]

    # Relationships to the Rating model
    ratings_given: Mapped[list["Rating"]] = relationship("Rating", foreign_keys="[Rating.rater_id]", back_populates="rater")
    ratings_received: Mapped[list["Rating"]] = relationship("Rating", foreign_keys="[Rating.rated_id]", back_populates="rated")

    @property
    def average_rating(self):
        if not self.ratings_received:
            return 0
        return sum(r.rating for r in self.ratings_received) / len(self.ratings_received)

    def set_password(self, password: str):
        # Hash the password before storing it in the database
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        # Check if the password is correct
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert user to dictionary"""
        result = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "pronouns": self.pronouns,
            "bio": self.bio,
            "location": self.location,
            "availability": self.availability,
            "learning_style": self.learning_style,
            "skills_to_offer": self.skills_to_offer,
            "skills_to_learn": self.skills_to_learn,
            "average_rating": self.average_rating,
            "image_url": self.image_url,
        }
        return result

    @classmethod
    def from_dict(cls, data):
        """Create user from dictionary data"""
        user = cls()
        user.name = data["name"]
        user.email = data["email"]
        user.pronouns = data.get("pronouns")
        user.bio = data.get("bio")
        user.location = data.get("location")
        user.availability = data.get("availability")
        user.learning_style = data.get("learning_style")
        user.skills_to_offer = data.get("skills_to_offer")
        user.skills_to_learn = data.get("skills_to_learn")
        user.image_url = data.get("image_url")
        if "password" in data:
            user.set_password(data["password"])
        return user
