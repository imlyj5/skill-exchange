# Skill Exchange Backend

Flask-based REST API for the Skill Exchange Platform, providing user authentication, skill matching, chat functionality, and file uploads.

### Technology Stack
- **Framework**: Flask 3.1.0
- **Database**: PostgreSQL with SQLAlchemy 2.0 ORM
- **Migrations**: Alembic
- **AI Integration**: Google Gemini API
- **File Processing**: Pillow (PIL)
- **CORS**: Flask-CORS
- **Testing**: pytest

### Project Structure
```
backend/
├── app/                    # Main application package
│   ├── __init__.py        
│   ├── config.py          # Configuration settings
│   ├── db.py              # Database setup
│   ├── models/            # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py        # User model
│   │   ├── chat.py        # Chat model
│   │   ├── message.py     # Message model
│   │   └── rating.py      # Rating model
│   └── routes/            # API endpoints
│       ├── __init__.py
│       ├── auth.py        # Authentication routes
│       ├── profile.py     # User profile routes
│       ├── match.py       # Matching routes
│       ├── chat.py        # Chat routes
│       ├── ratings.py     # Rating routes
│       ├── upload.py      # File upload routes
│       └── route_utilities.py  # Shared utilities
├── migrations/            # Database migrations
├── uploads/              # File upload storage
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
└── README.md            
```

## Quick Start

### Prerequisites
- Python
- PostgreSQL
- Google Gemini API key (optional)

### Installation

1. **Navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   # Create .env file
   # Database Configuration
   SQLALCHEMY_DATABASE_URI=postgresql://skill_user:your_password@localhost:5432/skill_exchange
   # AI Integration (optional)
   GEMINI_API_KEY=your-gemini-api-key-here

5. **Set up database**
   ```bash
   # Create database
   psql postgres
   CREATE DATABASE skill_exchange;
   \q
   
   # Run migrations
   flask db upgrade
   ```

6. **Start the server**
   ```bash
   flask run
   ```

The API will be available at `http://localhost:5000`

### Database Models

#### User Model
```python
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
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
```

#### Chat Model
```python
class Chat(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user1_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user2_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
```

#### Message Model
```python
class Message(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False)
```

#### Rating Model
```python
class Rating(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    rater_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    rated_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[Optional[str]]
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
```

### API Endpoints

#### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

#### Profiles
- `GET /profile/{user_id}` - Get user profile
- `PUT /profile/{user_id}` - Update user profile

#### Matching
- `GET /matches/{user_id}` - Get potential matches

#### Chat
- `GET /chats/{user_id}` - Get user's chats
- `POST /chats` - Create new chat
- `GET /chats/{chat_id}/messages` - Get chat messages
- `POST /chats/{chat_id}/messages` - Send message
- `DELETE /chats/{chat_id}` - Delete chat

#### Ratings
- `GET /ratings/{user_id}` - Get user ratings
- `POST /ratings` - Create rating

#### File Upload
- `POST /upload/profile-image/{user_id}` - Upload profile image
- `DELETE /upload/profile-image/{user_id}` - Delete profile image
- `GET /upload/uploads/{filename}` - Serve uploaded files

### AI Integration

The backend includes AI-powered skill matching using Google Gemini API:

- **Intelligent Matching**: Matches related skills (e.g., "violin" ↔ "music")
- **Bidirectional Matching**: Both users must be able to teach and learn
- **Graceful Fallback**: Falls back to exact matching if AI is unavailable
- **Rate Limiting**: 100ms delay between API calls

For detailed AI setup, see the [AI Setup Guide](../docs/SETUP_AI.md).

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

### Test Database
```bash
# From project root
./scripts/test-db.sh
```

### Migration Commands
```bash
# Create new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

## File Uploads

### Supported Formats
- PNG, JPG, JPEG
- Maximum size: 5MB
- Automatic resizing to 800x800 pixels

### Storage
- Files stored in `uploads/profile_images/`
- Unique filenames to prevent conflicts
- Automatic cleanup of old profile images

### Security
- File type validation using magic numbers
- Size limit enforcement