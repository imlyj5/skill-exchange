# Backend (Flask API)

This directory contains the Flask backend for the Skill Exchange platform.

## Manual Setup Instructions

### 1. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
- Create a `.env` file in this directory with the following content (edit values as needed):

```
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost:5432/your_db_name
GEMINI_API_KEY=your-gemini-api-key (Optional)
```

### 4. Create the PostgreSQL database
```bash
createdb your_db_name
```

### 5. Run database migrations
```bash
flask db upgrade
```

### 6. Run the backend server
```bash
flask run
```

## Testing

To run backend tests:
```bash
python -m pytest
```

## Technology Stack
- **Framework**: Flask 3.1.0
- **Database**: PostgreSQL with SQLAlchemy 2.0 ORM
- **Migrations**: Alembic
- **AI Integration**: Google Gemini API
- **File Processing**: Pillow (PIL)
- **CORS**: Flask-CORS
- **Testing**: pytest

## Project Structure
```
backend/
├── app/                    # Main application package
│   ├── models/            # SQLAlchemy models
│   └── routes/            # API endpoints
├── migrations/            # Database migrations
├── uploads/               # File upload storage
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
└── README.md            
```

The API will be available at `http://localhost:5000`

## More
- For database schema and models, see [../docs/DATABASE.md](../docs/DATABASE.md)
- For API endpoints and usage, see [../docs/API.md](../docs/API.md)
- For AI integration, see [../docs/SETUP_AI.md](../docs/SETUP_AI.md)

---

For overall project info, see the root README.