# Complete Setup Guide

This guide provides step-by-step instructions for setting up the Skill Exchange Platform from scratch.

## 🎯 Overview

The Skill Exchange Platform consists of:
- **Backend**: Flask API with PostgreSQL database
- **Frontend**: React application
- **AI Integration**: Google Gemini API for intelligent matching

## 📋 Prerequisites

### System Requirements
- **Operating System**: macOS, Linux, or Windows
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **PostgreSQL**: 12 or higher
- **Git**: For version control

### Required Accounts
- **Google Gemini API**: For AI-powered matching (free tier available)

## 🚀 Quick Start (Automated)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd skill-exchange
```

### 2. Run Automated Setup
```bash
# This will set up both backend and frontend
./scripts/setup.sh
```

### 3. Set Up Database
```bash
# This will configure PostgreSQL and run migrations
./scripts/db-setup.sh
```

### 4. Start Development Servers
```bash
# This will start both backend and frontend
./scripts/dev.sh
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## 🔧 Manual Setup (Detailed)

### Step 1: Install System Dependencies

#### macOS
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PostgreSQL
brew install postgresql
brew services start postgresql

# Install Python dependencies
brew install libmagic
```

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Install Python dependencies
sudo apt install libmagic1
```

#### Windows
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Install with default settings
3. Download Python from https://www.python.org/downloads/
4. Install Node.js from https://nodejs.org/

### Step 2: Verify Installations

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check Node.js version
node --version     # Should be 16+

# Check PostgreSQL version
psql --version     # Should be 12+

# Check if PostgreSQL is running
# macOS
brew services list | grep postgresql

# Linux
sudo systemctl status postgresql
```

### Step 3: Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Database Configuration

#### Option A: Using the Setup Script
```bash
# From the project root
./scripts/db-setup.sh
```

#### Option B: Manual Database Setup

1. **Create Database and User**
   ```bash
   # Connect to PostgreSQL as superuser
   psql postgres
   
   # Create user and database
   CREATE USER skill_user WITH PASSWORD 'your_secure_password';
   CREATE DATABASE skill_exchange OWNER skill_user;
   GRANT ALL PRIVILEGES ON DATABASE skill_exchange TO skill_user;
   \q
   ```

2. **Create Environment File**
   ```bash
   cd backend
   
   # Create .env file
   cat > .env << EOF
   # Database Configuration
   SQLALCHEMY_DATABASE_URI=postgresql://skill_user:your_secure_password@localhost:5432/skill_exchange
   
   # AI Integration (see SETUP_AI.md for detailed setup)
   GEMINI_API_KEY=your-gemini-api-key-here
   
   # Flask Configuration
   FLASK_ENV=development
   FLASK_DEBUG=1
   SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
   
   # CORS Configuration
   CORS_ORIGINS=http://localhost:3000,http://localhost:3001
   EOF
   ```

3. **Run Database Migrations**
   ```bash
   # Make sure virtual environment is activated
   source venv/bin/activate
   
   # Run migrations
   flask db upgrade
   ```

### Step 5: Frontend Setup

```bash
cd frontend

# Install Node.js dependencies
npm install
```

### Step 6: AI Setup (Optional)

For AI-powered skill matching, follow the dedicated setup guide:
- **📖 [AI Setup Guide](SETUP_AI.md)** - Complete instructions for Google Gemini API setup

### Step 7: Test the Setup

```bash
# Test database connection
./scripts/test-db.sh

# Start backend server
cd backend
source venv/bin/activate
flask run

# In another terminal, start frontend
cd frontend
npm start
```

## 🧪 Testing Your Setup

### Database Tests
```bash
# Run comprehensive database tests
./scripts/test-db.sh
```

### Backend Tests
```bash
cd backend
source venv/bin/activate
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔍 Troubleshooting

### Common Issues

#### 1. PostgreSQL Connection Issues
```bash
# Check if PostgreSQL is running
# macOS
brew services list | grep postgresql

# Linux
sudo systemctl status postgresql

# Start PostgreSQL if not running
# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

#### 2. Permission Issues
```bash
# Fix PostgreSQL permissions (Linux)
sudo chown -R postgres:postgres /var/lib/postgresql
sudo chmod 700 /var/lib/postgresql/data
```

#### 3. Migration Issues
```bash
# Check migration status
flask db current

# Reset migrations (WARNING: This will lose data)
flask db stamp head
flask db migrate
flask db upgrade
```

#### 4. Port Conflicts
```bash
# Check if ports are in use
lsof -i :5000  # Backend port
lsof -i :3000  # Frontend port

# Kill processes if needed
kill -9 <PID>
```

#### 5. Virtual Environment Issues
```bash
# Recreate virtual environment
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 6. Node.js Issues
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Environment-Specific Issues

#### macOS Issues
```bash
# If you get libmagic errors
brew install libmagic

# If PostgreSQL won't start
brew services restart postgresql
```

#### Linux Issues
```bash
# If you get permission errors
sudo chown -R $USER:$USER ~/.npm
sudo chown -R $USER:$USER ~/.config

# If PostgreSQL won't start
sudo systemctl restart postgresql
```

#### Windows Issues
```bash
# If you get path issues, add to PATH:
# C:\Program Files\PostgreSQL\14\bin
# C:\Users\YourUser\AppData\Local\Programs\Python\Python38\Scripts

# If you get permission errors, run as Administrator
```

## 📊 Verification Checklist

After setup, verify the following:

- [ ] PostgreSQL is running and accessible
- [ ] Database `skill_exchange` exists
- [ ] All tables are created (users, chats, messages, ratings)
- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] API endpoints are accessible
- [ ] Frontend can connect to backend
- [ ] Google Gemini API key is configured (optional - see [AI Setup Guide](SETUP_AI.md))
- [ ] File uploads work (PNG, JPG, JPEG only)
- [ ] All tests pass

## 🚀 Next Steps

Once setup is complete:

1. **Explore the Application**
   - Register a new user
   - Create a profile with skills to offer and learn
   - Test the AI-powered matching system
   - Try the chat functionality
   - Upload a profile picture

2. **Development Workflow**
   - Make changes to the code
   - Run tests before committing
   - Use the development scripts (`./scripts/dev.sh`)

3. **Deployment**
   - Review the deployment guide in `docs/DEPLOYMENT.md`
   - Choose a deployment platform
   - Set up production environment

## 📚 Additional Resources

- **📖 [API Documentation](API.md)** - Complete API reference
- **🗄️ [Database Documentation](DATABASE.md)** - Database schema and operations
- **🚀 [Deployment Guide](DEPLOYMENT.md)** - Production deployment instructions
- **🤖 [AI Setup Guide](SETUP_AI.md)** - Google Gemini API setup
- **👥 [Contributing Guidelines](CONTRIBUTING.md)** - Development guidelines

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs** for error messages
2. **Review this guide** for troubleshooting steps
3. **Search existing issues** in the project repository
4. **Create a new issue** with detailed information
5. **Contact the development team**

## 🔧 Development Scripts

The project includes several helpful scripts:

- `./scripts/setup.sh` - Automated setup for both backend and frontend
- `./scripts/db-setup.sh` - Database setup and migration
- `./scripts/dev.sh` - Start both development servers
- `./scripts/test-db.sh` - Test database connectivity

## 📝 Project Structure

```
skill-exchange/
├── backend/          # Flask API server
│   ├── app/         # Application code
│   │   ├── models/  # Database models
│   │   ├── routes/  # API endpoints
│   │   └── config.py
│   ├── migrations/  # Database migrations
│   ├── uploads/     # File uploads
│   └── requirements.txt
├── frontend/        # React application
│   ├── src/         # Source code
│   │   ├── components/  # React components
│   │   └── assets/      # Static assets
│   ├── public/      # Static files
│   └── package.json
├── scripts/         # Development and deployment scripts
└── docs/           # Documentation
```

---

**Happy coding! 🎉**

Your Skill Exchange Platform is now ready for development and deployment. 