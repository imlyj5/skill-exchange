#!/bin/bash

# Database Test Script for Skill Exchange Platform
# This script tests the database connection and basic functionality

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
        print('✅ Database connection successful!')
        print(f'📊 PostgreSQL version: {result.fetchone()[0]}')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
"
    
    cd ..
}

# Test database tables
test_tables() {
    print_status "Testing database tables..."
    
    cd backend
    
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Test tables using Python
    python3 -c "
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))

try:
    with engine.connect() as conn:
        # Check if tables exist - using the actual schema
        tables = ['users', 'chats', 'messages', 'ratings']
        for table in tables:
            result = conn.execute(text(f\"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}');\"))
            exists = result.fetchone()[0]
            if exists:
                print(f'✅ Table {table} exists')
            else:
                print(f'❌ Table {table} missing')
                exit(1)
        
        print('✅ All required tables exist!')
        
        # Check table counts
        for table in tables:
            result = conn.execute(text(f'SELECT COUNT(*) FROM {table};'))
            count = result.fetchone()[0]
            print(f'📊 {table}: {count} records')
            
except Exception as e:
    print(f'❌ Table test failed: {e}')
    exit(1)
"
    
    cd ..
}

# Test Flask app
test_flask_app() {
    print_status "Testing Flask application..."
    
    cd backend
    
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Test Flask app
    python3 -c "
import os
from dotenv import load_dotenv
from app import create_app, db
from sqlalchemy import text

load_dotenv()
app = create_app()

with app.app_context():
    try:
        # Test database connection through Flask
        with db.engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        print('✅ Flask app database connection successful!')
        
        # Test basic app functionality
        print('✅ Flask app initialization successful!')
        
    except Exception as e:
        print(f'❌ Flask app test failed: {e}')
        exit(1)
"
    
    cd ..
}

# Test API endpoints (if server is running)
test_api_endpoints() {
    print_status "Testing API endpoints..."
    
    # Check if server is running on port 5000
    if curl -s http://localhost:5000 > /dev/null 2>&1; then
        print_success "Backend server is running on port 5000"
        
        # Test health endpoint (if it exists)
        if curl -s http://localhost:5000/health > /dev/null 2>&1; then
            print_success "Health endpoint is accessible"
        else
            print_warning "Health endpoint not found (this is normal)"
        fi
        
        # Test CORS headers
        CORS_HEADERS=$(curl -s -I -H "Origin: http://localhost:3000" http://localhost:5000 | grep -i "access-control-allow-origin" || echo "")
        if [ ! -z "$CORS_HEADERS" ]; then
            print_success "CORS headers are properly configured"
        else
            print_warning "CORS headers not found (check configuration)"
        fi
        
    else
        print_warning "Backend server is not running on port 5000"
        print_status "To test API endpoints, start the server with: cd backend && flask run"
    fi
}

# Test migrations
test_migrations() {
    print_status "Testing database migrations..."
    
    cd backend
    
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Check migration status
    CURRENT_MIGRATION=$(flask db current 2>/dev/null || echo "No migrations")
    print_status "Current migration: $CURRENT_MIGRATION"
    
    # Check if migrations are up to date
    flask db check 2>/dev/null && print_success "Migrations are up to date" || print_warning "Migrations may need to be applied"
    
    cd ..
}

# Main function
main() {
    echo "🧪 Database and Application Test Suite"
    echo "======================================"
    
    test_connection
    test_tables
    test_flask_app
    test_migrations
    test_api_endpoints
    
    echo ""
    print_success "All tests completed!"
    echo ""
    echo "If all tests passed, your database and application are ready!"
    echo ""
    echo "Next steps:"
    echo "1. Start the backend: cd backend && source venv/bin/activate && flask run"
    echo "2. Start the frontend: cd frontend && npm start"
    echo "3. Access the application at http://localhost:3000"
    echo ""
}

# Run main function
main "$@" 