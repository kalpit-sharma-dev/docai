#!/bin/bash

# PS-05 Document Understanding System - Quick Start Script
# This script automates the setup and initial run of the PS-05 system

set -e  # Exit on any error

echo "🚀 PS-05 Document Understanding System - Quick Start"
echo "=================================================="

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

# Check if we're in the right directory
if [ ! -f "ps05.py" ]; then
    print_error "Please run this script from the project root directory (where ps05.py is located)"
    exit 1
fi

# Check Python version
print_status "Checking Python version..."
python_version=$(python --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 0 ]]; then
    print_error "Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi
print_success "Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_warning "Some dependencies failed to install. This is normal for optional packages like polyglot on Windows."
    print_status "Continuing with core dependencies..."
fi
print_success "Python dependencies installed"

# Check if YOLOv8 model exists
if [ ! -f "yolov8x.pt" ]; then
    print_warning "YOLOv8 model not found. The system will download it automatically on first run."
else
    print_success "YOLOv8 model found"
fi

# Test backend installation
print_status "Testing backend installation..."
python ps05.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Backend installation verified"
else
    print_error "Backend installation failed"
    exit 1
fi

# Setup frontend
print_status "Setting up frontend..."
cd frontend

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16.x or higher"
    exit 1
fi

node_version=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$node_version" -lt 16 ]; then
    print_error "Node.js 16.x or higher is required. Found: $(node --version)"
    exit 1
fi
print_success "Node.js version: $(node --version)"

# Install frontend dependencies
print_status "Installing frontend dependencies..."
npm install --legacy-peer-deps
print_success "Frontend dependencies installed"

# Test frontend installation
print_status "Testing frontend installation..."
npx expo --version > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Frontend installation verified"
else
    print_error "Frontend installation failed"
    exit 1
fi

cd ..

# Run demo
print_status "Running demo to verify system functionality..."
python demo.py
print_success "Demo completed successfully"

echo ""
echo "🎉 Setup completed successfully!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Start the API server: python ps05.py server"
echo "2. Start the mobile app: cd frontend && npm start"
echo "3. View API docs: http://localhost:8000/docs"
echo ""
echo "For detailed instructions, see: SETUP_AND_RUN.md"
echo "" 