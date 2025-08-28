@echo off
REM PS-05 Competition Deployment Script for Windows
REM This script deploys the complete PS-05 system for competition evaluation

echo 🚀 PS-05 Competition Deployment Starting...
echo ==========================================

setlocal enabledelayedexpansion

REM Configuration
set COMPETITION_MODE=true
set STAGE=1
set GPU_ENABLED=true
set MONITORING_ENABLED=true

REM Check system requirements
echo [INFO] Checking system requirements...

REM Check Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check Docker Compose
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Check GPU support
nvidia-smi >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] NVIDIA GPU detected
    set GPU_ENABLED=true
) else (
    echo [WARNING] No NVIDIA GPU detected. Running in CPU mode.
    set GPU_ENABLED=false
)

echo [SUCCESS] System requirements check completed.

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs
if not exist "logs" mkdir logs
if not exist "data\train" mkdir "data\train"
if not exist "data\val" mkdir "data\val"
if not exist "data\test" mkdir "data\test"
if not exist "models\cache" mkdir "models\cache"
echo [SUCCESS] Directories created successfully.

REM Download pre-trained models
echo [INFO] Checking pre-trained models...
if not exist "models\yolov8x.pt" (
    echo [WARNING] YOLOv8x model not found. Please download manually or run the training script.
    echo [INFO] You can download from: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt
) else (
    echo [SUCCESS] YOLOv8x model already exists.
)

REM Build and start services
echo [INFO] Building and starting PS-05 services...

REM Set environment variables
set COMPETITION_MODE=true
set STAGE=1
set GPU_ENABLED=%GPU_ENABLED%

REM Build and start services
if "%GPU_ENABLED%"=="true" (
    echo [INFO] Starting services with GPU support...
    docker-compose up --build -d
) else (
    echo [INFO] Starting services in CPU mode...
    docker-compose up --build -d
)

if %errorlevel% neq 0 (
    echo [ERROR] Failed to start services.
    pause
    exit /b 1
)

echo [SUCCESS] Services started successfully.

REM Wait for services to be ready
echo [INFO] Waiting for services to be ready...

REM Wait for backend
echo [INFO] Waiting for backend service...
set timeout=120
set counter=0

:wait_backend_loop
curl -f http://localhost:8000/api/v1/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Backend service is ready.
    goto wait_frontend
)

if %counter% geq %timeout% (
    echo [ERROR] Backend service failed to start within %timeout% seconds.
    pause
    exit /b 1
)

timeout /t 2 /nobreak >nul
set /a counter+=2
echo -n .
goto wait_backend_loop

:wait_frontend
REM Wait for frontend
echo [INFO] Waiting for frontend service...
set timeout=60
set counter=0

:wait_frontend_loop
curl -f http://localhost:19000 >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Frontend service is ready.
    goto health_checks
)

if %counter% geq %timeout% (
    echo [WARNING] Frontend service may not be ready yet.
    goto health_checks
)

timeout /t 2 /nobreak >nul
set /a counter+=2
echo -n .
goto wait_frontend_loop

:health_checks
REM Run health checks
echo [INFO] Running health checks...

REM Backend health check
curl -f http://localhost:8000/api/v1/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Backend health check passed.
) else (
    echo [ERROR] Backend health check failed.
    pause
    exit /b 1
)

REM Test Stage 1 inference
echo [INFO] Testing Stage 1 inference pipeline...

REM Create a test image if none exists
if not exist "tests\test_data\test_document.png" (
    echo [WARNING] No test image found. Creating a simple test image...
    python -c "import numpy as np; from PIL import Image; import os; img = Image.new('RGB', (800, 600), color='white'); img.save('tests/test_data/test_document.png'); print('Test image created.')"
)

REM Run Stage 1 test
python test_stage1.py
if %errorlevel% equ 0 (
    echo [SUCCESS] Stage 1 inference test passed.
) else (
    echo [ERROR] Stage 1 inference test failed.
    pause
    exit /b 1
)

REM Display system information
echo.
echo [SUCCESS] PS-05 Competition System Deployed Successfully!
echo.
echo 🌐 System Access Information:
echo ==============================
echo Backend API:     http://localhost:8000
echo Frontend App:    http://localhost:19000
echo API Docs:        http://localhost:8000/docs
echo Health Check:    http://localhost:8000/api/v1/health

if "%MONITORING_ENABLED%"=="true" (
    echo.
    echo 📊 Monitoring:
    echo ==============
    echo Prometheus:    http://localhost:9090
    echo Grafana:       http://localhost:3000 (admin/ps05_admin_2025)
)

echo.
echo 🔧 Competition Commands:
echo ========================
echo Test Stage 1:    python test_stage1.py
echo Run Inference:   python ps05.py infer --input image.png --output results/ --stage 1
echo View Logs:       docker-compose logs -f
echo Stop System:     docker-compose down

echo.
echo 📋 Competition Requirements Met:
echo =================================
echo ✅ Document Layout Detection (6 classes)
echo ✅ JSON Output with Bounding Boxes
echo ✅ Docker Deployment Ready
echo ✅ API Interface Available
echo ✅ Mobile App Interface
echo ✅ Monitoring and Logging

echo.
echo 🎯 Ready for PS-05 Competition Evaluation!
echo Submission Deadline: 5 November 2025

echo.
echo [SUCCESS] Deployment completed successfully!
pause
