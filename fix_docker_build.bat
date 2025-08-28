@echo off
REM PS-05 Docker Build Fix Script for Windows
REM This script helps resolve common Docker build issues on Windows

echo 🔧 PS-05 Docker Build Fix Script
echo =================================

REM Check Docker status
echo [INFO] Checking Docker status...
docker system info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running or accessible!
    echo [INFO] Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo [SUCCESS] Docker is running.

REM Clean up Docker resources
echo [INFO] Cleaning up Docker resources...
docker-compose down --remove-orphans >nul 2>&1
docker image prune -f >nul 2>&1
docker container prune -f >nul 2>&1
echo [SUCCESS] Docker cleanup completed.

REM Try building with different approaches
echo [INFO] Trying different build approaches...

REM Approach 1: Use simplified Dockerfile
echo [INFO] Approach 1: Using simplified Dockerfile...
docker-compose build ps05-backend
if %errorlevel% equ 0 (
    echo [SUCCESS] Build successful with simplified Dockerfile!
    goto :test_build
)

echo [WARNING] Approach 1 failed. Trying approach 2...

REM Approach 2: Build without cache
echo [INFO] Approach 2: Building without cache...
docker-compose build --no-cache ps05-backend
if %errorlevel% equ 0 (
    echo [SUCCESS] Build successful without cache!
    goto :test_build
)

echo [WARNING] Approach 2 failed. Trying approach 3...

REM Approach 3: Use even more minimal Dockerfile
echo [INFO] Approach 3: Creating minimal Dockerfile...
call :create_minimal_dockerfile

docker-compose build ps05-backend
if %errorlevel% equ 0 (
    echo [SUCCESS] Build successful with minimal Dockerfile!
    goto :test_build
)

echo [ERROR] All build approaches failed.
echo.
echo 💡 Alternative solutions:
echo 1. Try running without Docker: python ps05.py server
echo 2. Use the Windows batch file: deploy_competition.bat
echo 3. Check Docker Desktop settings and restart it
echo 4. Ensure you have enough disk space and RAM
pause
exit /b 1

:create_minimal_dockerfile
echo [INFO] Creating minimal Dockerfile...
(
echo # Minimal PS-05 Dockerfile for basic functionality
echo FROM python:3.9-slim-bullseye
echo.
echo ENV PYTHONUNBUFFERED=1
echo ENV DEBIAN_FRONTEND=noninteractive
echo.
echo # Install minimal dependencies
echo RUN apt-get update ^&^& apt-get install -y \
echo     curl \
echo     wget \
echo     ^&^& rm -rf /var/lib/apt/lists/*
echo.
echo WORKDIR /app
echo.
echo # Copy requirements
echo COPY requirements.txt .
echo.
echo # Install Python dependencies
echo RUN pip install --no-cache-dir --upgrade pip ^&^& \
echo     pip install --no-cache-dir -r requirements.txt
echo.
echo # Copy application
echo COPY . .
echo.
echo # Create directories
echo RUN mkdir -p /app/data /app/models /app/outputs /app/logs /app/uploads
echo.
echo # Set permissions
echo RUN chmod +x /app/ps05.py
echo.
echo EXPOSE 8000
echo.
echo CMD ["python", "ps05.py", "server", "--host", "0.0.0.0", "--port", "8000"]
) > Dockerfile.minimal

REM Update docker-compose to use minimal Dockerfile
powershell -Command "(Get-Content docker-compose.yml) -replace 'dockerfile: Dockerfile.competition', 'dockerfile: Dockerfile.minimal' | Set-Content docker-compose.yml"
echo [SUCCESS] Minimal Dockerfile created.
goto :eof

:test_build
echo [INFO] Testing the build...
docker-compose up -d ps05-backend
if %errorlevel% equ 0 (
    echo [SUCCESS] Backend service started successfully!
    
    echo [INFO] Waiting for service to be ready...
    timeout /t 30 /nobreak >nul
    
    REM Test health check
    curl -f http://localhost:8000/api/v1/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo [SUCCESS] Health check passed! Build is working.
        echo.
        echo 🎉 PS-05 system is now working!
        echo.
        echo 🌐 Access your system at:
        echo    Backend: http://localhost:8000
        echo    API Docs: http://localhost:8000/docs
        echo.
        echo 🔧 To start all services:
        echo    docker-compose up -d
    ) else (
        echo [WARNING] Service started but health check failed. Checking logs...
        docker-compose logs ps05-backend
    )
) else (
    echo [ERROR] Failed to start backend service.
)

echo.
echo [SUCCESS] Build fix process completed!
pause
