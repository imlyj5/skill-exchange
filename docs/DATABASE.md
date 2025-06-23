# Database Documentation

This document provides comprehensive information about the database setup, schema, and management for the Skill Exchange Platform.

## Database Overview

The Skill Exchange Platform uses **PostgreSQL** as its primary database with **SQLAlchemy 2.0 ORM** for database operations and **Alembic** for migrations.

## Database Schema

### Tables

#### 1. Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    pronouns VARCHAR(100),
    bio TEXT,
    location VARCHAR(255),
    availability VARCHAR(255),
    learning_style VARCHAR(255),
    skills_to_offer VARCHAR(50)[],
    skills_to_learn VARCHAR(50)[],
    image_url VARCHAR(255)
);
```

**Fields:**
- `id`: Primary key, auto-incrementing
- `name`: User's full name
- `email`: Unique email address
- `password_hash`: Hashed password using Werkzeug
- `pronouns`: User's preferred pronouns
- `bio`: User's biography/description
- `location`: User's location (city, state, country)
- `availability`: User's availability for learning/teaching
- `learning_style`: User's preferred learning style
- `skills_to_offer`: PostgreSQL array of skills user can teach
- `skills_to_learn`: PostgreSQL array of skills user wants to learn
- `image_url`: URL to user's profile image

#### 2. Chats Table
```sql
CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    user1_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    user2_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id`: Primary key, auto-incrementing
- `user1_id`: Foreign key to first user
- `user2_id`: Foreign key to second user
- `created_at`: When the chat was created (with timezone)

#### 3. Messages Table
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    chat_id INTEGER REFERENCES chats(id) ON DELETE CASCADE NOT NULL,
    sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE NOT NULL
);
```

**Fields:**
- `id`: Primary key, auto-incrementing
- `chat_id`: Foreign key to chats table
- `sender_id`: Foreign key to users table (who sent the message)
- `content`: Message text content
- `timestamp`: When the message was sent (with timezone)
- `is_read`: Whether the message has been read

#### 4. Ratings Table
```sql
CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    rater_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    rated_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    chat_id INTEGER REFERENCES chats(id) ON DELETE CASCADE NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id`: Primary key, auto-incrementing
- `rater_id`: Foreign key to users table (who gave the rating)
- `rated_id`: Foreign key to users table (who received the rating)
- `chat_id`: Foreign key to chats table (which chat the rating is for)
- `rating`: Rating value (1-5 stars)
- `comment`: Optional comment about the experience
- `timestamp`: When the rating was created (with timezone)

## Database Setup

### Prerequisites

1. **Install PostgreSQL**
   ```bash
   # macOS
   brew install postgresql
   brew services start postgresql
   
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   
   # Windows
   # Download from https://www.postgresql.org/download/windows/
   ```

2. **Verify Installation**
   ```bash
   psql --version
   ```

### Automated Setup

Use the provided setup script:
```bash
./scripts/db-setup.sh
```

This script will:
- Check PostgreSQL installation
- Create database and user
- Configure environment variables
- Run migrations
- Test connection
- Optionally create sample data

### Manual Setup

1. **Create Database and User**
   ```bash
   # Connect to PostgreSQL as superuser
   psql postgres
   
   # Create user and database
   CREATE USER skill_user WITH PASSWORD 'your_password';
   CREATE DATABASE skill_exchange OWNER skill_user;
   GRANT ALL PRIVILEGES ON DATABASE skill_exchange TO skill_user;
   \q
   ```

2. **Configure Environment**
   Create `backend/.env`:
   ```env
   SQLALCHEMY_DATABASE_URI=postgresql://skill_user:your_password@localhost:5432/skill_exchange
   GEMINI_API_KEY=your-gemini-api-key-here
   FLASK_ENV=development
   FLASK_DEBUG=1
   SECRET_KEY=your-secret-key-here
   ```

3. **Run Migrations**
   ```bash
   cd backend
   source venv/bin/activate
   flask db upgrade
   ```

## Database Models

### User Model
```python
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

    # Relationships
    ratings_given: Mapped[list["Rating"]] = relationship("Rating", foreign_keys="[Rating.rater_id]", back_populates="rater")
    ratings_received: Mapped[list["Rating"]] = relationship("Rating", foreign_keys="[Rating.rated_id]", back_populates="rated")
    
    @property
    def average_rating(self):
        if not self.ratings_received:
            return 0
        return sum(r.rating for r in self.ratings_received) / len(self.ratings_received)
```

### Chat Model
```python
class Chat(db.Model):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user1_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user2_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    # Relationships
    user1: Mapped["User"] = relationship("User", foreign_keys=[user1_id], backref="chats_as_user1")
    user2: Mapped["User"] = relationship("User", foreign_keys=[user2_id], backref="chats_as_user2")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
```

### Message Model
```python
class Message(db.Model):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Relationships
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
    sender: Mapped["User"] = relationship("User", backref="messages_sent")
```

### Rating Model
```python
class Rating(db.Model):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rater_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    rated_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[Optional[str]]
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    # Relationships
    rater: Mapped["User"] = relationship("User", foreign_keys=[rater_id], back_populates="ratings_given")
    rated: Mapped["User"] = relationship("User", foreign_keys=[rated_id], back_populates="ratings_received")
    chat: Mapped["Chat"] = relationship("Chat", backref="ratings")
```

## Migrations

### Migration Commands

```bash
# Initialize migrations (first time only)
flask db init

# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade

# Show migration history
flask db history

# Show current migration
flask db current
```

### Existing Migrations

1. **Initial Migration** (`e9f553e1ebf6_.py`)
   - Creates all base tables

2. **Add Rating Model** (`1dffc659eeb6_add_rating_model_and_relationships.py`)
   - Adds ratings table and relationships

3. **Add Image URL** (`3e0e781efaa2_add_image_url_to_users_table.py`)
   - Adds image_url field to users table

4. **Add Is Read** (`880cde487140_add_is_read_to_message_model.py`)
   - Adds is_read field to messages table

## Database Operations

### Common Queries

#### Get User with Skills
```python
user = User.query.filter_by(email='john@example.com').first()
print(f"User: {user.name}")
print(f"Teaches: {user.skills_to_offer}")
print(f"Wants to learn: {user.skills_to_learn}")
print(f"Average rating: {user.average_rating}")
```

#### Get User's Chats
```python
# Get chats where user is user1
chats_as_user1 = Chat.query.filter_by(user1_id=user_id).all()
# Get chats where user is user2
chats_as_user2 = Chat.query.filter_by(user2_id=user_id).all()
# Combine both
all_chats = chats_as_user1 + chats_as_user2
```

#### Get Chat Messages
```python
messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
```

#### Get User Ratings
```python
ratings = Rating.query.filter_by(rated_id=user_id).all()
average_rating = db.session.query(func.avg(Rating.rating)).filter_by(rated_id=user_id).scalar()
```

### Performance Optimization

#### Indexes
```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_chats_user1_id ON chats(user1_id);
CREATE INDEX idx_chats_user2_id ON chats(user2_id);
CREATE INDEX idx_messages_chat_id ON messages(chat_id);
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_ratings_rated_id ON ratings(rated_id);
CREATE INDEX idx_ratings_chat_id ON ratings(chat_id);
```

#### Connection Pooling
```python
# In app configuration
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}
```

## Backup and Recovery

### Backup Database
```bash
# Create backup
pg_dump skill_exchange > backup_$(date +%Y%m%d_%H%M%S).sql

# Create compressed backup
pg_dump skill_exchange | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

### Restore Database
```bash
# Restore from backup
psql skill_exchange < backup_20240115_143000.sql

# Restore from compressed backup
gunzip -c backup_20240115_143000.sql.gz | psql skill_exchange
```

### Automated Backups
```bash
#!/bin/bash
# backup_script.sh
BACKUP_DIR="/path/to/backups"
DB_NAME="skill_exchange"
DATE=$(date +%Y%m%d_%H%M%S)

pg_dump $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 7 days of backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

Add to crontab:
```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup_script.sh
```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   ```bash
   # Check if PostgreSQL is running
   sudo systemctl status postgresql
   
   # Start PostgreSQL
   sudo systemctl start postgresql
   ```

2. **Permission Denied**
   ```bash
   # Check PostgreSQL logs
   sudo tail -f /var/log/postgresql/postgresql-*.log
   
   # Fix permissions
   sudo chown -R postgres:postgres /var/lib/postgresql
   ```

3. **Migration Errors**
   ```bash
   # Check migration status
   flask db current
   
   # Reset migrations (WARNING: This will lose data)
   flask db stamp head
   flask db migrate
   flask db upgrade
   ```

### Performance Issues

1. **Slow Queries**
   ```sql
   -- Enable query logging
   ALTER SYSTEM SET log_statement = 'all';
   SELECT pg_reload_conf();
   ```

2. **Connection Pool Exhaustion**
   ```python
   # Increase pool size
   app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
       'pool_size': 20,
       'max_overflow': 30
   }
   ```

## Security Considerations

1. **Use Environment Variables**
   - Never hardcode database credentials
   - Use `.env` files for configuration

2. **Database Permissions**
   ```sql
   -- Create read-only user for analytics
   CREATE USER readonly_user WITH PASSWORD 'password';
   GRANT CONNECT ON DATABASE skill_exchange TO readonly_user;
   GRANT USAGE ON SCHEMA public TO readonly_user;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
   ```

3. **Encrypt Connections**
   ```python
   # Use SSL connections in production
   SQLALCHEMY_DATABASE_URI = "postgresql://user:pass@host:port/db?sslmode=require"
   ```

4. **Regular Updates**
   - Keep PostgreSQL updated
   - Monitor security advisories
   - Apply security patches promptly

## Monitoring

### Database Metrics
```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('skill_exchange'));

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check active connections
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
```

### Log Monitoring
```bash
# Monitor PostgreSQL logs
tail -f /var/log/postgresql/postgresql-*.log | grep -E "(ERROR|WARNING)"

# Monitor slow queries
tail -f /var/log/postgresql/postgresql-*.log | grep "duration:"
``` 