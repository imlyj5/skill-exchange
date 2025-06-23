# Skill Exchange Platform

A full-stack web application that connects people for skill sharing and learning. Users can find matches based on their skills, location, and preferences using AI-powered matching algorithms.

## 🚀 Features

- **AI-Powered Matching**: Intelligent skill matching using Google Gemini API
- **Location-Based Sorting**: Find users near you for in-person meetups
- **Real-Time Chat**: Connect and communicate with your matches
- **Profile Management**: Upload images and manage your skills
- **Rating System**: Rate and review your learning experiences
- **User Authentication**: Secure login and registration system

## 📁 Project Structure

```
skill-exchange/
├── backend/                 # Flask API server
│   ├── app/                # Main application code
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   └── __init__.py     # Flask app initialization
│   ├── migrations/         # Database migrations
│   ├── uploads/           # File uploads directory
│   ├── requirements.txt   # Python dependencies
│   └── README.md          # Backend documentation
├── frontend/              # React client application
│   ├── src/               # Source code
│   │   ├── components/    # React components
│   │   └── assets/        # Static assets
│   ├── public/            # Public assets
│   ├── package.json       # Node.js dependencies
│   └── README.md          # Frontend documentation
├── docs/                  # Project documentation
│   ├── API.md            # API documentation
│   ├── DATABASE.md       # Database setup and schema
│   ├── DEPLOYMENT.md     # Deployment guide
│   └── CONTRIBUTING.md   # Contributing guidelines
├── scripts/               # Utility scripts
│   ├── setup.sh          # Automated setup script
│   ├── dev.sh            # Development server script
│   └── db-setup.sh       # Database setup script
├── README.md             # This file
├── .gitignore            # Git ignore rules
└── LICENSE               # MIT license
```

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python 3.8+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Integration**: Google Gemini API
- **File Uploads**: Pillow for image processing
- **Authentication**: Session-based auth
- **CORS**: Flask-CORS for cross-origin requests
- **Migrations**: Alembic

### Frontend
- **Framework**: React 18
- **HTTP Client**: Axios
- **Styling**: CSS modules
- **Build Tool**: Create React App

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Google Gemini API key

### Option 1: Automated Setup (Recommended)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd skill-exchange

# 2. Run the automated setup script
./scripts/setup.sh

# 3. Set up the database
./scripts/db-setup.sh

# 4. Start development servers
./scripts/dev.sh
```

### Option 2: Manual Setup

#### 1. Backend Setup
```bash
cd backend

# Install system dependencies (macOS)
brew install libmagic

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost/skill_exchange"
export GEMINI_API_KEY="your-gemini-api-key-here"

# Initialize the database
flask db upgrade

# Run the application
flask run
```

#### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

#### 3. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 🔧 Environment Variables

Create a `.env` file in the backend directory:

```env
# Database Configuration
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/skill_exchange

# AI Integration
GEMINI_API_KEY=your-gemini-api-key-here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# File Upload Configuration
MAX_CONTENT_LENGTH=5242880
UPLOAD_FOLDER=uploads
```

## 🗄️ Database Setup

### Quick Database Setup
```bash
# Run the database setup script
./scripts/db-setup.sh
```

### Manual Database Setup
1. **Install PostgreSQL**
   ```bash
   # macOS
   brew install postgresql
   brew services start postgresql
   
   # Ubuntu/Debian
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   ```

2. **Create Database and User**
   ```sql
   CREATE USER skill_user WITH PASSWORD 'your_password';
   CREATE DATABASE skill_exchange OWNER skill_user;
   GRANT ALL PRIVILEGES ON DATABASE skill_exchange TO skill_user;
   ```

3. **Run Migrations**
   ```bash
   cd backend
   source venv/bin/activate
   flask db upgrade
   ```

For detailed database documentation, see [docs/DATABASE.md](docs/DATABASE.md).

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user

### Profile Endpoints
- `GET /profile/<user_id>` - Get user profile
- `PUT /profile/<user_id>` - Update user profile

### Matching Endpoints
- `GET /match/<user_id>` - Get potential matches
- `POST /match/<user_id>/like/<target_id>` - Like a user
- `POST /match/<user_id>/dislike/<target_id>` - Dislike a user

### Chat Endpoints
- `GET /chats/<user_id>` - Get user's chats
- `POST /chats` - Create new chat
- `GET /chats/<chat_id>/messages` - Get chat messages
- `POST /chats/<chat_id>/messages` - Send message

### File Upload Endpoints
- `POST /upload/profile-image/<user_id>` - Upload profile image
- `DELETE /upload/profile-image/<user_id>` - Delete profile image

For complete API documentation, see [docs/API.md](docs/API.md).

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Backend Deployment Options
- **Heroku**: Easy deployment with PostgreSQL add-on
- **DigitalOcean App Platform**: Managed deployment
- **AWS EC2**: Full control over infrastructure
- **Docker**: Containerized deployment

### Frontend Deployment Options
- **Vercel**: Optimized for React apps
- **Netlify**: Easy static site hosting
- **AWS S3 + CloudFront**: Scalable static hosting
- **GitHub Pages**: Free hosting for open source

For detailed deployment instructions, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`./scripts/test.sh`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. **Check Documentation**: Review the docs in the `docs/` directory
2. **Search Issues**: Look for similar issues in the GitHub issues
3. **Create Issue**: Open a new issue with detailed information
4. **Contact**: Reach out to the development team

### Common Issues

#### Database Connection Issues
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -h localhost -U skill_user -d skill_exchange
```

#### Migration Issues
```bash
# Check migration status
flask db current

# Reset migrations (WARNING: This will lose data)
flask db stamp head
flask db migrate
flask db upgrade
```

#### Frontend Build Issues
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

## 🔮 Roadmap

### Planned Features
- [ ] Real-time notifications
- [ ] Video chat integration
- [ ] Mobile app development
- [ ] Advanced search filters
- [ ] Skill verification system
- [ ] Community features
- [ ] Payment integration
- [ ] Multi-language support

### Performance Improvements
- [ ] Database query optimization
- [ ] Caching implementation
- [ ] CDN integration
- [ ] Image optimization
- [ ] Lazy loading

## 📊 Project Status

- **Backend**: ✅ Complete with AI integration
- **Frontend**: ✅ Complete with modern UI
- **Database**: ✅ PostgreSQL with migrations
- **Documentation**: ✅ Comprehensive docs
- **Testing**: ✅ Unit and integration tests
- **Deployment**: ✅ Multiple deployment options

## 🙏 Acknowledgments

- **Google Gemini API** for AI-powered matching
- **Flask** community for the excellent web framework
- **React** team for the amazing frontend library
- **PostgreSQL** for the reliable database
- **Open Source Community** for all the amazing tools

---

**Made with ❤️ by the Skill Exchange Team**

Connect, Learn, Grow Together! 🌟
