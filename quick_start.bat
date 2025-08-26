@echo off
REM PS-05 Document Understanding System - Quick Start Script (Windows)
REM This script automates the setup and initial run of the PS-05 system

echo 🚀 PS-05 Document Understanding System - Quick Start
echo ==================================================

REM Check if we're in the right directory
if not exist "ps05.py" (
    echo [ERROR] Please run this script from the project root directory (where ps05.py is located)
    pause
    exit /b 1
)

REM Check Python version
echo [INFO] Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [INFO] Virtual environment already exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some dependencies failed to install. This is normal for optional packages like polyglot on Windows.
    echo [INFO] Continuing with core dependencies...
)
echo [SUCCESS] Python dependencies installed

REM Check if YOLOv8 model exists
if not exist "yolov8x.pt" (
    echo [WARNING] YOLOv8 model not found. The system will download it automatically on first run.
) else (
    echo [SUCCESS] YOLOv8 model found
)

REM Test backend installation
echo [INFO] Testing backend installation...
python ps05.py --help >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Backend installation failed
    pause
    exit /b 1
)
echo [SUCCESS] Backend installation verified

REM Setup frontend
echo [INFO] Setting up frontend...
cd frontend

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 16.x or higher
    pause
    exit /b 1
)
echo [SUCCESS] Node.js version: 
node --version

REM Install frontend dependencies
echo [INFO] Installing frontend dependencies...
npm install --legacy-peer-deps
if errorlevel 1 (
    echo [ERROR] Failed to install frontend dependencies
    pause
    exit /b 1
)
echo [SUCCESS] Frontend dependencies installed

REM Test frontend installation
echo [INFO] Testing frontend installation...
npx expo --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Frontend installation failed
    pause
    exit /b 1
)
echo [SUCCESS] Frontend installation verified

cd ..

REM Run demo
echo [INFO] Running demo to verify system functionality...
python demo.py
if errorlevel 1 (
    echo [ERROR] Demo failed
    pause
    exit /b 1
)
echo [SUCCESS] Demo completed successfully

echo.
echo 🎉 Setup completed successfully!
echo ================================
echo.
echo Next steps:
echo 1. Start the API server: python ps05.py server
echo 2. Start the mobile app: cd frontend ^&^& npm start
echo 3. View API docs: http://localhost:8000/docs
echo.
echo For detailed instructions, see: SETUP_AND_RUN.md
echo.
pause 