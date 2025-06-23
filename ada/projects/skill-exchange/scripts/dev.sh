#!/bin/bash

# Skill Exchange Platform Development Script
# This script starts both backend and frontend servers for development

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

# Function to cleanup background processes on exit
cleanup() {
    print_status "Shutting down servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    print_success "Servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check if backend is ready
check_backend() {
    local max_attempts=30
    local attempt=1
    
    print_status "Waiting for backend to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:5000/health > /dev/null 2>&1; then
            print_success "Backend is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 1
        attempt=$((attempt + 1))
    done
    
    print_warning "Backend may not be fully ready, but continuing..."
    return 1
}

# Start backend server
start_backend() {
    print_status "Starting backend server..."
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_error "Backend virtual environment not found. Run ./scripts/setup.sh first."
        exit 1
    fi
    
    # Activate virtual environment and start Flask
    source venv/bin/activate
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating default .env file..."
        cat > .env << EOF
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/skill_exchange
GEMINI_API_KEY=your-gemini-api-key-here
FLASK_ENV=development
FLASK_DEBUG=1
EOF
        print_warning "Please update backend/.env with your actual credentials"
    fi
    
    # Start Flask server in background
    flask run --host=0.0.0.0 --port=5000 &
    BACKEND_PID=$!
    
    cd ..
    
    print_success "Backend server started (PID: $BACKEND_PID)"
}

# Start frontend server
start_frontend() {
    print_status "Starting frontend server..."
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_error "Frontend dependencies not found. Run ./scripts/setup.sh first."
        exit 1
    fi
    
    # Start React development server in background
    npm start &
    FRONTEND_PID=$!
    
    cd ..
    
    print_success "Frontend server started (PID: $FRONTEND_PID)"
}

# Main function
main() {
    echo "🚀 Starting Skill Exchange Platform Development Servers"
    echo "======================================================"
    
    # Start backend first
    start_backend
    
    # Wait a moment for backend to initialize
    sleep 2
    
    # Check if backend is ready (optional)
    check_backend
    
    # Start frontend
    start_frontend
    
    echo ""
    print_success "Both servers are starting up!"
    echo ""
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:5000"
    echo ""
    echo "Press Ctrl+C to stop both servers"
    echo ""
    
    # Wait for user to stop servers
    wait
}

# Run main function
main "$@" 