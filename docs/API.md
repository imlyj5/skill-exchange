# API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication

login/register endpoints require authentication. 

## Endpoints

### Authentication

#### Register User
```http
POST /auth/signup
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "John",
  "email": "john@gmail.com",
  "password": "testpassword"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John",
  "email": "john@gmail.com",
  "message": "User created successfully"
}
```

#### Login User
```http
POST /auth/login
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "john@gmail.com",
  "password": "testpassword"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user_id": 1,
  "name": "John"
}
```

#### Logout User
```http
POST /auth/logout
```

**Response:**
```json
{
  "message": "Logout successful"
}
```

### Profiles

#### Get User Profile
```http
GET /profile/{user_id}
```

**Response:**
```json
{
  "id": 1,
  "name": "John",
  "email": "john@gmail.com",
  "bio": "I love teaching and learning new skills!",
  "location": "San Francisco, CA",
  "skills_to_offer": ["Python", "JavaScript", "Cooking"],
  "skills_to_learn": ["Guitar", "Spanish"],
  "image_url": "/upload/uploads/profile_images/profile_1_20241201_143022_abc12345.jpg",
  "average_rating": 4.5,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Update User Profile
```http
PUT /profile/{user_id}
Content-Type: application/json
```

**Request Body:**
```json
{
  "bio": "Updated bio text",
  "location": "New York, NY",
  "skills_to_offer": ["Python", "JavaScript", "Cooking", "Photography"],
  "skills_to_learn": ["Guitar", "Spanish", "Yoga"]
}
```

**Response:**
```json
{
  "message": "Profile updated successfully"
}
```

### File Uploads

#### Upload Profile Image
```http
POST /upload/profile-image/{user_id}
Content-Type: multipart/form-data
```

**Form Data:**
- `image`: File (PNG, JPG, JPEG, max 5MB)

**Response:**
```json
{
  "message": "Profile image uploaded successfully",
  "image_url": "/upload/uploads/profile_images/profile_1_20241201_143022_abc12345.jpg",
  "filename": "profile_1_20241201_143022_abc12345.jpg"
}
```

#### Delete Profile Image
```http
DELETE /upload/profile-image/{user_id}
```

**Response:**
```json
{
  "message": "Profile image deleted successfully"
}
```

#### Serve Uploaded Files
```http
GET /upload/uploads/{filename}
```

**Response:**
Returns the actual file content (images, etc.)

### Matching

#### Get Potential Matches
```http
GET /matches/{user_id}
```

**Response:**
```json
{
  "matches": [
    {
      "id": 2,
      "name": "Jane",
      "email": "jane@gmail.com",
      "bio": "Passionate about music and languages",
      "location": "San Francisco, CA",
      "skills_to_offer": ["Guitar", "Spanish"],
      "skills_to_learn": ["Python", "Cooking"],
      "image_url": "/upload/uploads/profile_images/profile_2_20241201_143055_def67890.jpg",
      "average_rating": 4.8,
      "offer_matches": ["Python matches Python", "Cooking matches Cooking"],
      "learn_matches": ["Guitar matches Guitar", "Spanish matches Spanish"]
    }
  ],
  "count": 1,
  "ai_enabled": true
}
```

**Notes:**
- `offer_matches`: Skills the user can teach to the candidate
- `learn_matches`: Skills the user can learn from the candidate
- `ai_enabled`: Whether AI matching is available
- Matches only include users where both can teach and learn from each other

**AI Matching**: For detailed information about AI-powered skill matching, see the [AI Setup Guide](SETUP_AI.md).

### Chat

#### Get User's Chats
```http
GET /chats/{user_id}
```

**Response:**
```json
{
  "chats": [
    {
      "id": 1,
      "user1_id": 1,
      "user2_id": 2,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

#### Create New Chat
```http
POST /chats
Content-Type: application/json
```

**Request Body:**
```json
{
  "user1_id": 1,
  "user2_id": 2
}
```

**Response:**
```json
{
  "message": "Chat created successfully",
  "chat_id": 1
}
```

#### Get Chat Messages
```http
GET /chats/{chat_id}/messages
```

**Response:**
```json
{
  "messages": [
    {
      "id": 1,
      "content": "Hi! I saw we matched for Python and Guitar lessons",
      "sender_id": 1,
      "timestamp": "2024-01-15T10:05:00Z",
      "is_read": true
    },
    {
      "id": 2,
      "content": "Yes! I'd love to learn Python from you",
      "sender_id": 2,
      "timestamp": "2024-01-15T10:10:00Z",
      "is_read": true
    }
  ]
}
```

#### Send Message
```http
POST /chats/{chat_id}/messages
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "Great! When would you like to meet?",
  "sender_id": 1
}
```

**Response:**
```json
{
  "message": "Message sent successfully",
  "message_id": 6
}
```

#### Delete Chat
```http
DELETE /chats/{chat_id}
```

**Response:**
```json
{
  "message": "Chat deleted successfully"
}
```

#### Mark Messages as Read
```http
PUT /chats/{chat_id}/messages/read
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": 1
}
```

**Response:**
```json
{
  "message": "Messages marked as read"
}
```

### Ratings

#### Get User Ratings
```http
GET /ratings/{user_id}
```

**Response:**
```json
{
  "ratings": [
    {
      "id": 1,
      "rater_id": 2,
      "rated_id": 1,
      "rating": 5,
      "comment": "Excellent Python teacher! Very patient and clear explanations.",
      "skill": "Python",
      "created_at": "2024-01-15T16:00:00Z"
    }
  ],
  "average_rating": 4.8,
  "total_ratings": 5
}
```

#### Create Rating
```http
POST /ratings
Content-Type: application/json
```

**Request Body:**
```json
{
  "rater_id": 2,
  "rated_id": 1,
  "rating": 5,
  "comment": "Excellent Python teacher! Very patient and clear explanations.",
  "skill": "Python"
}
```

**Response:**
```json
{
  "message": "Rating created successfully",
  "rating_id": 1
}
```

## Error Responses
### 400 Bad Request
```json
{
  "error": "Invalid request data",
  "details": "Specific error message"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "error": "Access denied"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Rate Limiting

API requests are rate-limited to prevent abuse. Limits are:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

## CORS

The API supports CORS for cross-origin requests from the frontend application.

## File Upload Limits

- Maximum file size: 5MB
- Supported formats: PNG, JPG, JPEG
- Files are stored in the `/uploads/profile_images/` directory
- Images are automatically resized to max 800x800 pixels
- Old profile images are automatically cleaned up (keeps only the most recent)

## Additional Resources

- **[AI Setup Guide](SETUP_AI.md)** - Google Gemini API setup and AI matching details
- **[Database Documentation](DATABASE.md)** - Database schema and operations 