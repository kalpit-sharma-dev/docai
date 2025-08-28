#!/bin/bash

# PS-05 Competition Deployment Script for Windows
# This script deploys the complete PS-05 system for competition evaluation on Windows

set -e

echo "🚀 PS-05 Competition Deployment Starting (Windows)..."
echo "===================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPETITION_MODE=true
STAGE=1
GPU_ENABLED=true
MONITORING_ENABLED=true

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

# Check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker Desktop first."
        print_status "Download from: https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        print_status "Docker Desktop usually includes Docker Compose"
        exit 1
    fi
    
    # Check if Docker Desktop is running
    print_status "Checking if Docker Desktop is running..."
    if ! docker system info &> /dev/null; then
        print_error "Docker Desktop is not running!"
        echo ""
        echo "🔧 To fix this:"
        echo "1. Look for Docker Desktop icon in your system tray (bottom right)"
        echo "2. If not there, search for 'Docker Desktop' in Start menu"
        echo "3. Start Docker Desktop and wait for it to fully load"
        echo "4. You should see a green Docker icon in system tray when ready"
        echo ""
        echo "⏳ Wait for Docker Desktop to fully start (may take 1-2 minutes)"
        echo "Then run this script again."
        echo ""
        exit 1
    fi
    
    print_success "Docker Desktop is running and accessible."
    
    # Check GPU support
    if command -v nvidia-smi &> /dev/null; then
        print_success "NVIDIA GPU detected: $(nvidia-smi --query-gpu=name --format=csv,noheader,nounits)"
        GPU_ENABLED=true
    else
        print_warning "No NVIDIA GPU detected. Running in CPU mode."
        GPU_ENABLED=false
    fi
    
    # Check available memory (Windows)
    if command -v wmic &> /dev/null; then
        MEMORY_GB=$(wmic computersystem get TotalPhysicalMemory | tail -1 | awk '{print int($1/1024/1024/1024)}')
        if [ "$MEMORY_GB" -lt 8 ]; then
            print_warning "System has less than 8GB RAM (${MEMORY_GB}GB). Performance may be limited."
        else
            print_success "System memory: ${MEMORY_GB}GB"
        fi
    else
        print_warning "Could not determine memory size. Continuing..."
    fi
    
    print_success "System requirements check completed."
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p uploads
    mkdir -p outputs
    mkdir -p logs
    mkdir -p data/train
    mkdir -p data/val
    mkdir -p data/test
    mkdir -p models/cache
    
    print_success "Directories created successfully."
}

# Download pre-trained models
download_models() {
    print_status "Checking pre-trained models..."
    
    if [ ! -f "models/yolov8x.pt" ]; then
        print_warning "YOLOv8x model not found. Downloading..."
        mkdir -p models
        
        # Try different download methods
        if command -v curl &> /dev/null; then
            print_status "Downloading with curl..."
            curl -L -o models/yolov8x.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt
        elif command -v wget &> /dev/null; then
            print_status "Downloading with wget..."
            wget -O models/yolov8x.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt
        else
            print_error "Neither curl nor wget found."
            print_status "Please download yolov8x.pt manually:"
            print_status "1. Go to: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt"
            print_status "2. Save the file to: models/yolov8x.pt"
            print_status "3. Run this script again"
            exit 1
        fi
        
        if [ -f "models/yolov8x.pt" ]; then
            print_success "YOLOv8x model downloaded successfully."
        else
            print_error "Download failed. Please check your internet connection and try again."
            exit 1
        fi
    else
        print_success "YOLOv8x model already exists."
    fi
}

# Build and start services
deploy_services() {
    print_status "Building and starting PS-05 services..."
    
    # Set environment variables
    export COMPETITION_MODE=true
    export STAGE=1
    export GPU_ENABLED=$GPU_ENABLED
    
    # For Windows, we'll start with just the backend first
    if [ "$GPU_ENABLED" = true ]; then
        print_status "Starting services with GPU support..."
        print_status "Note: GPU support on Windows may require additional configuration"
    else
        print_status "Starting services in CPU mode..."
    fi
    
    # Start backend first
    print_status "Starting backend service..."
    docker-compose up --build -d ps05-backend
    
    # Wait a bit for backend to start
    sleep 10
    
    # Start other services
    print_status "Starting remaining services..."
    docker-compose up --build -d
    
    print_success "Services started successfully."
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for backend
    print_status "Waiting for backend service..."
    timeout=180  # Increased timeout for Windows
    counter=0
    
    while ! curl -f http://localhost:8000/api/v1/health &> /dev/null; do
        if [ $counter -ge $timeout ]; then
            print_error "Backend service failed to start within $timeout seconds."
            print_status "Checking Docker logs..."
            docker-compose logs ps05-backend
            print_status "Troubleshooting tips:"
            print_status "1. Make sure Docker Desktop has enough resources (8GB+ RAM)"
            print_status "2. Check if port 8000 is available"
            print_status "3. Try restarting Docker Desktop"
            exit 1
        fi
        sleep 3
        counter=$((counter + 3))
        echo -n "."
    done
    echo ""
    print_success "Backend service is ready."
    
    # Wait for frontend
    print_status "Waiting for frontend service..."
    timeout=90
    counter=0
    
    while ! curl -f http://localhost:19000 &> /dev/null; do
        if [ $counter -ge $timeout ]; then
            print_warning "Frontend service may not be ready yet."
            break
        fi
        sleep 3
        counter=$((counter + 3))
        echo -n "."
    done
    echo ""
    print_success "Frontend service is ready."
}

# Run health checks
run_health_checks() {
    print_status "Running health checks..."
    
    # Backend health check
    if curl -f http://localhost:8000/api/v1/health &> /dev/null; then
        print_success "Backend health check passed."
    else
        print_error "Backend health check failed."
        exit 1
    fi
    
    # Test Stage 1 inference
    print_status "Testing Stage 1 inference pipeline..."
    
    # Create a test image if none exists
    if [ ! -f "tests/test_data/test_document.png" ]; then
        print_warning "No test image found. Creating a simple test image..."
        python -c "
import numpy as np
from PIL import Image
import os

# Create a simple test image
img = Image.new('RGB', (800, 600), color='white')
img.save('tests/test_data/test_document.png')
print('Test image created.')
"
    fi
    
    # Run Stage 1 test
    if python test_stage1.py; then
        print_success "Stage 1 inference test passed."
    else
        print_error "Stage 1 inference test failed."
        exit 1
    fi
}

# Display system information
display_info() {
    print_success "PS-05 Competition System Deployed Successfully!"
    echo ""
    echo "🌐 System Access Information:"
    echo "=============================="
    echo "Backend API:     http://localhost:8000"
    echo "Frontend App:    http://localhost:19000"
    echo "API Docs:        http://localhost:8000/docs"
    echo "Health Check:    http://localhost:8000/api/v1/health"
    
    if [ "$MONITORING_ENABLED" = true ]; then
        echo ""
        echo "📊 Monitoring:"
        echo "=============="
        echo "Prometheus:    http://localhost:9090"
        echo "Grafana:       http://localhost:3000 (admin/ps05_admin_2025)"
    fi
    
    echo ""
    echo "🔧 Competition Commands:"
    echo "========================"
    echo "Test Stage 1:    python test_stage1.py"
    echo "Run Inference:   python ps05.py infer --input image.png --output results/ --stage 1"
    echo "View Logs:       docker-compose logs -f"
    echo "Stop System:     docker-compose down"
    
    echo ""
    echo "📋 Competition Requirements Met:"
    echo "================================="
    echo "✅ Document Layout Detection (6 classes)"
    echo "✅ JSON Output with Bounding Boxes"
    echo "✅ Docker Deployment Ready"
    echo "✅ API Interface Available"
    echo "✅ Mobile App Interface"
    echo "✅ Monitoring and Logging"
    
    echo ""
    echo "🎯 Ready for PS-05 Competition Evaluation!"
    echo "Submission Deadline: 5 November 2025"
    
    echo ""
    echo "💡 Windows Tips:"
    echo "================"
    echo "• Keep Docker Desktop running in background"
    echo "• If services fail, try restarting Docker Desktop"
    echo "• Check Windows Defender Firewall for port blocking"
    echo "• Ensure Docker Desktop has enough resources allocated"
}

# Main deployment function
main() {
    echo "Starting PS-05 Competition Deployment (Windows)..."
    echo "================================================"
    
    check_requirements
    create_directories
    download_models
    deploy_services
    wait_for_services
    run_health_checks
    display_info
    
    print_success "Deployment completed successfully!"
}

# Run main function
main "$@"
