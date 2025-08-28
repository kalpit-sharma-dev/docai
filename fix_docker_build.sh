#!/bin/bash

# PS-05 Docker Build Fix Script
# This script helps resolve common Docker build issues

set -e

echo "🔧 PS-05 Docker Build Fix Script"
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check Docker status
check_docker() {
    print_status "Checking Docker status..."
    
    if ! docker system info &> /dev/null; then
        print_error "Docker is not running or accessible!"
        print_status "Please start Docker Desktop and try again."
        exit 1
    fi
    
    print_success "Docker is running."
}

# Clean up Docker resources
cleanup_docker() {
    print_status "Cleaning up Docker resources..."
    
    # Stop and remove containers
    docker-compose down --remove-orphans 2>/dev/null || true
    
    # Remove old images
    docker image prune -f 2>/dev/null || true
    
    # Remove old containers
    docker container prune -f 2>/dev/null || true
    
    print_success "Docker cleanup completed."
}

# Try building with different approaches
try_build_approaches() {
    print_status "Trying different build approaches..."
    
    # Approach 1: Use simplified Dockerfile
    print_status "Approach 1: Using simplified Dockerfile..."
    if docker-compose build ps05-backend; then
        print_success "Build successful with simplified Dockerfile!"
        return 0
    fi
    
    print_warning "Approach 1 failed. Trying approach 2..."
    
    # Approach 2: Build without cache
    print_status "Approach 2: Building without cache..."
    if docker-compose build --no-cache ps05-backend; then
        print_success "Build successful without cache!"
        return 0
    fi
    
    print_warning "Approach 2 failed. Trying approach 3..."
    
    # Approach 3: Use even more minimal Dockerfile
    print_status "Approach 3: Creating minimal Dockerfile..."
    create_minimal_dockerfile
    
    if docker-compose build ps05-backend; then
        print_success "Build successful with minimal Dockerfile!"
        return 0
    fi
    
    print_error "All build approaches failed."
    return 1
}

# Create a minimal Dockerfile for basic functionality
create_minimal_dockerfile() {
    print_status "Creating minimal Dockerfile..."
    
    cat > Dockerfile.minimal << 'EOF'
# Minimal PS-05 Dockerfile for basic functionality
FROM python:3.9-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install minimal dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p /app/data /app/models /app/outputs /app/logs /app/uploads

# Set permissions
RUN chmod +x /app/ps05.py

EXPOSE 8000

CMD ["python", "ps05.py", "server", "--host", "0.0.0.0", "--port", "8000"]
EOF

    # Update docker-compose to use minimal Dockerfile
    sed -i 's/dockerfile: Dockerfile.competition/dockerfile: Dockerfile.minimal/' docker-compose.yml
    
    print_success "Minimal Dockerfile created."
}

# Test the build
test_build() {
    print_status "Testing the build..."
    
    if docker-compose up -d ps05-backend; then
        print_success "Backend service started successfully!"
        
        # Wait for service to be ready
        print_status "Waiting for service to be ready..."
        sleep 30
        
        # Test health check
        if curl -f http://localhost:8000/api/v1/health &> /dev/null; then
            print_success "Health check passed! Build is working."
            return 0
        else
            print_warning "Service started but health check failed. Checking logs..."
            docker-compose logs ps05-backend
            return 1
        fi
    else
        print_error "Failed to start backend service."
        return 1
    fi
}

# Main function
main() {
    echo "Starting Docker build fix process..."
    
    check_docker
    cleanup_docker
    try_build_approaches
    
    if [ $? -eq 0 ]; then
        print_success "Build fixed successfully!"
        
        if test_build; then
            print_success "🎉 PS-05 system is now working!"
            echo ""
            echo "🌐 Access your system at:"
            echo "   Backend: http://localhost:8000"
            echo "   API Docs: http://localhost:8000/docs"
            echo ""
            echo "🔧 To start all services:"
            echo "   docker-compose up -d"
        else
            print_warning "Build succeeded but service test failed. Check logs above."
        fi
    else
        print_error "Failed to fix Docker build issues."
        echo ""
        echo "💡 Alternative solutions:"
        echo "1. Try running without Docker: python ps05.py server"
        echo "2. Use the Windows batch file: deploy_competition.bat"
        echo "3. Check Docker Desktop settings and restart it"
        echo "4. Ensure you have enough disk space and RAM"
    fi
}

# Run main function
main "$@"
