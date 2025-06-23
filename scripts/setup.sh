#!/bin/bash

# Skill Exchange Platform Setup Script
# This script sets up the development environment for both backend and frontend

set -e  # Exit on any error

echo "🚀 Setting up Skill Exchange Platform..."

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

# Check if required tools are installed
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8+"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 16+"
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm"
        exit 1
    fi
    
    # Check PostgreSQL (optional but recommended)
    if ! command -v psql &> /dev/null; then
        print_warning "PostgreSQL is not installed. You'll need to install it manually."
        print_warning "For macOS: brew install postgresql"
        print_warning "For Ubuntu: sudo apt-get install postgresql postgresql-contrib"
    fi
    
    print_success "System requirements check completed"
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Install system dependencies on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        print_status "Installing system dependencies (macOS)..."
        if ! command -v brew &> /dev/null; then
            print_warning "Homebrew not found. Please install libmagic manually."
        else
            brew install libmagic
        fi
    fi
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        print_status "Creating .env file..."
        cat > .env << EOF
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/skill_exchange
GEMINI_API_KEY=your-gemini-api-key-here
FLASK_ENV=development
FLASK_DEBUG=1
EOF
        print_warning "Please update the .env file with your actual database credentials and API keys"
    fi
    
    # Create uploads directory
    mkdir -p uploads
    
    print_success "Backend setup completed"
    cd ..
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install Node.js dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    print_success "Frontend setup completed"
    cd ..
}

# Create git hooks
setup_git_hooks() {
    print_status "Setting up Git hooks..."
    
    # Create .git/hooks directory if it doesn't exist
    mkdir -p .git/hooks
    
    # Create pre-commit hook
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

echo "Running pre-commit checks..."

# Check Python syntax in backend
cd backend
if command -v python3 &> /dev/null; then
    python3 -m py_compile app/__init__.py
    echo "✓ Python syntax check passed"
fi

# Check JavaScript syntax in frontend
cd ../frontend
if command -v npm &> /dev/null; then
    npm run build --silent
    echo "✓ JavaScript build check passed"
fi

echo "Pre-commit checks completed successfully!"
EOF
    
    # Make the hook executable
    chmod +x .git/hooks/pre-commit
    
    print_success "Git hooks setup completed"
}

# Main setup function
main() {
    echo "🎯 Skill Exchange Platform Setup"
    echo "================================"
    
    check_requirements
    setup_backend
    setup_frontend
    setup_git_hooks
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Update backend/.env with your database credentials and API keys"
    echo "2. Start the backend: cd backend && source venv/bin/activate && flask run"
    echo "3. Start the frontend: cd frontend && npm start"
    echo "4. Access the application at http://localhost:3000"
    echo ""
    echo "For more information, see the README.md file"
}

# Run main function
main "$@" 