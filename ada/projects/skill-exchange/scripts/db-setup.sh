#!/bin/bash

# Database Setup Script for Skill Exchange Platform
# This script helps set up PostgreSQL and run migrations

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if PostgreSQL is installed
check_postgresql() {
    print_status "Checking PostgreSQL installation..."
    
    if ! command -v psql &> /dev/null; then
        print_error "PostgreSQL is not installed."
        echo ""
        echo "Installation instructions:"
        echo ""
        echo "macOS:"
        echo "  brew install postgresql"
        echo "  brew services start postgresql"
        echo ""
        echo "Ubuntu/Debian:"
        echo "  sudo apt update"
        echo "  sudo apt install postgresql postgresql-contrib"
        echo "  sudo systemctl start postgresql"
        echo "  sudo systemctl enable postgresql"
        echo ""
        echo "Windows:"
        echo "  Download from https://www.postgresql.org/download/windows/"
        echo ""
        exit 1
    fi
    
    print_success "PostgreSQL is installed"
}

# Setup PostgreSQL database
setup_database() {
    print_status "Setting up PostgreSQL database..."
    
    # Get database configuration
    read -p "Enter database name [skill_exchange]: " DB_NAME
    DB_NAME=${DB_NAME:-skill_exchange}
    
    read -p "Enter database username [skill_user]: " DB_USER
    DB_USER=${DB_USER:-skill_user}
    
    read -s -p "Enter database password: " DB_PASSWORD
    echo ""
    
    read -p "Enter database host [localhost]: " DB_HOST
    DB_HOST=${DB_HOST:-localhost}
    
    read -p "Enter database port [5432]: " DB_PORT
    DB_PORT=${DB_PORT:-5432}
    
    # Create database and user
    print_status "Creating database and user..."
    
    # Connect as postgres superuser to create database and user
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS - usually no password for postgres user
        psql postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" || print_warning "User might already exist"
        psql postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" || print_warning "Database might already exist"
        psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    else
        # Linux - might need sudo
        sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" || print_warning "User might already exist"
        sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" || print_warning "Database might already exist"
        sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    fi
    
    # Create .env file with database configuration
    print_status "Creating .env file..."
    
    cd backend
    
    cat > .env << EOF
# Database Configuration
SQLALCHEMY_DATABASE_URI=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME

# AI Integration
GEMINI_API_KEY=your-gemini-api-key-here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# File Upload Configuration
MAX_CONTENT_LENGTH=5242880
UPLOAD_FOLDER=uploads
EOF
    
    print_success "Database configuration saved to backend/.env"
    print_warning "Please update GEMINI_API_KEY with your actual API key"
    
    cd ..
}

# Run database migrations
run_migrations() {
    print_status "Running database migrations..."
    
    cd backend
    
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Check if migrations directory exists
    if [ ! -d "migrations" ]; then
        print_status "Initializing migrations..."
        flask db init
    fi
    
    # Run migrations
    print_status "Applying migrations..."
    flask db upgrade
    
    cd ..
    
    print_success "Database migrations completed"
}

# Test database connection
test_connection() {
    print_status "Testing database connection..."
    
    cd backend
    
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Test connection using Python
    python3 -c "
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))
try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT version();'))
        print('Database connection successful!')
        print(f'PostgreSQL version: {result.fetchone()[0]}')
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
"
    
    cd ..
}

# Create sample data (optional)
create_sample_data() {
    read -p "Would you like to create sample data? (y/n): " CREATE_SAMPLE
    if [[ $CREATE_SAMPLE =~ ^[Yy]$ ]]; then
        print_status "Creating sample data..."
        
        cd backend
        
        # Activate virtual environment if it exists
        if [ -d "venv" ]; then
            source venv/bin/activate
        fi
        
        # Create sample data script
        cat > create_sample_data.py << 'EOF'
from app import create_app, db
from app.models.user import User
from app.models.chat import Chat
from app.models.message import Message
from werkzeug.security import generate_password_hash

def create_sample_data():
    app = create_app()
    with app.app_context():
        # Create sample users
        users = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'password': 'password123',
                'first_name': 'John',
                'last_name': 'Doe',
                'bio': 'I love teaching and learning new skills!',
                'location': 'San Francisco, CA',
                'skills_to_teach': ['Python', 'JavaScript', 'Cooking'],
                'skills_to_learn': ['Guitar', 'Spanish']
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'password': 'password123',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'bio': 'Passionate about music and languages',
                'location': 'San Francisco, CA',
                'skills_to_teach': ['Guitar', 'Spanish', 'Photography'],
                'skills_to_learn': ['Python', 'Cooking']
            },
            {
                'username': 'mike_wilson',
                'email': 'mike@example.com',
                'password': 'password123',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'bio': 'Fitness enthusiast and yoga instructor',
                'location': 'Oakland, CA',
                'skills_to_teach': ['Yoga', 'Fitness Training', 'Meditation'],
                'skills_to_learn': ['Cooking', 'Photography']
            }
        ]
        
        for user_data in users:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password']),
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                bio=user_data['bio'],
                location=user_data['location'],
                skills_to_teach=user_data['skills_to_teach'],
                skills_to_learn=user_data['skills_to_learn']
            )
            db.session.add(user)
        
        db.session.commit()
        print("Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data()
EOF
        
        python3 create_sample_data.py
        rm create_sample_data.py
        
        cd ..
        
        print_success "Sample data created"
    fi
}

# Main function
main() {
    echo "🗄️  Database Setup for Skill Exchange Platform"
    echo "=============================================="
    
    check_postgresql
    setup_database
    run_migrations
    test_connection
    create_sample_data
    
    echo ""
    print_success "Database setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Update backend/.env with your Gemini API key"
    echo "2. Start the backend: cd backend && source venv/bin/activate && flask run"
    echo "3. Start the frontend: cd frontend && npm start"
    echo "4. Access the application at http://localhost:3000"
    echo ""
    echo "Database connection string:"
    echo "postgresql://[username]:[password]@[host]:[port]/[database]"
    echo ""
}

# Run main function
main "$@" 