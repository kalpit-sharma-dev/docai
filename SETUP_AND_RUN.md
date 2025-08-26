# PS-05 Document Understanding System - Setup & Run Guide

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Running the System](#running-the-system)
6. [API Usage](#api-usage)
7. [CLI Usage](#cli-usage)
8. [Mobile App Usage](#mobile-app-usage)
9. [Troubleshooting](#troubleshooting)

## 🎯 System Overview

The PS-05 Intelligent Multilingual Document Understanding System consists of:

- **Backend**: Python FastAPI server with ML pipeline
- **Frontend**: React Native/Expo mobile application
- **CLI Tools**: Command-line interface for processing
- **API**: RESTful API for document processing
- **Models**: Layout detection, OCR, language identification, NL generation

### Supported Languages
- English, Hindi, Urdu, Arabic, Nepali, Persian

### Processing Stages
- **Stage 1**: Layout detection (Background, Text, Title, List, Table, Figure)
- **Stage 2**: Layout + OCR + Language identification
- **Stage 3**: Full analysis (Layout + OCR + Natural Language generation)

## 🔧 Prerequisites

### System Requirements
- **OS**: Windows 10/11, macOS, or Ubuntu 20.04+
- **Python**: 3.8-3.10
- **Node.js**: 16.x or higher
- **Git**: Latest version
- **Memory**: 8GB RAM minimum (16GB recommended)
- **Storage**: 10GB free space

### Hardware (Optional)
- **GPU**: NVIDIA GPU with CUDA support (for faster processing)
- **Camera**: For mobile app document capture

## 🐍 Backend Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd docai_full
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Pre-trained Models
```bash
# YOLOv8 model (already included)
# The yolov8x.pt file should be in the root directory
```

### 5. Verify Backend Installation
```bash
python ps05.py --help
```

Expected output:
```
usage: ps05.py [-h] {infer,train,eval,server,pack,overlay} ...

PS-05 Intelligent Multilingual Document Understanding System
```

### **Frontend Setup (React Native/Expo SDK 53)**

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (Expo SDK 53)
npm install --legacy-peer-deps

# Start development server
npm start
# or
npx expo start
```

**Frontend Technologies:**
- **Expo SDK 53** (latest stable)
- **React Native 0.76.3** (latest stable)
- **React 18.3.1** (latest stable)
- **TypeScript 5.3.0** (latest stable)
- **React Native Paper** (Material Design components)
- **React Navigation v6** (navigation)

## 🚀 Running the System

### Option 1: Quick Demo (Recommended for First Run)

#### 1. Run the Demo Script
```bash
# From root directory
python demo.py
```

This will:
- Create a sample document
- Process it through all 3 stages
- Generate output files in `demo_output/`
- Show performance metrics

Expected output:
```
🚀 PS-05 Document Understanding System Demo
📄 Creating sample document...
🔧 Initializing PS-05 pipeline...
📊 Stage 1: Layout Detection
📝 Stage 2: OCR and Language Identification
🤖 Stage 3: Natural Language Generation
💾 Results saved to demo_output/
✅ Demo completed successfully!
```

#### 2. View Results
```bash
# Check generated files
ls demo_output/
# sample_document.png, stage1_results.json, stage2_results.json, stage3_results.json
```

### Option 2: API Server Mode

#### 1. Start the Backend Server
```bash
# From root directory
python ps05.py server --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Starting PS-05 API server on 0.0.0.0:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 2. Access API Documentation
Open browser and go to: `http://localhost:8000/docs`

#### 3. Test API Endpoints
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Get system info
curl http://localhost:8000/api/v1/info

# Process document (replace with your image)
curl -X POST "http://localhost:8000/api/v1/infer?stage=3" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@demo_output/sample_document.png"
```

### Option 3: CLI Mode

#### 1. Single Image Processing
```bash
# Process single image
python ps05.py infer --input demo_output/sample_document.png --output results/ --stage 3
```

#### 2. Batch Processing
```bash
# Process multiple images
python ps05.py infer --input data/images/ --output results/ --batch --stage 3
```

#### 3. Create Submission Package
```bash
# Create challenge submission
python ps05.py pack --input demo_output/sample_document.png --output submission/ --stage 3
```

#### 4. Generate Overlay Visualization
```bash
# Create overlay image for QA
python ps05.py overlay --image demo_output/sample_document.png --json results/result.json --stage 3 --out overlay.png
```

### Option 4: Mobile App

#### 1. Start Frontend Development Server
```bash
cd frontend
npm start
```

#### 2. Run on Device/Simulator

**For Android:**
```bash
# Install Android Studio and set up emulator
npm run android
```

**For iOS:**
```bash
# Install Xcode (macOS only)
npm run ios
```

**For Web:**
```bash
npm run web
```

**For Expo Go (Mobile):**
```bash
# Install Expo Go app on your phone
# Scan QR code from terminal
```

## 📊 API Usage

### Available Endpoints

#### Health Check
```bash
GET /api/v1/health
```

#### System Information
```bash
GET /api/v1/info
```

#### Document Processing
```bash
POST /api/v1/infer?stage={1|2|3}
Content-Type: multipart/form-data
Body: file (image file)
```

### Example API Calls

#### Using curl
```bash
# Process document with stage 3
curl -X POST "http://localhost:8000/api/v1/infer?stage=3" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.png"
```

#### Using Python requests
```python
import requests

url = "http://localhost:8000/api/v1/infer"
files = {"file": open("document.png", "rb")}
params = {"stage": 3}

response = requests.post(url, files=files, params=params)
result = response.json()
print(result)
```

## 🖥️ CLI Usage

### Available Commands

#### Inference
```bash
# Single image
python ps05.py infer --input image.png --output results/ --stage 3

# Batch processing
python ps05.py infer --input images/ --output results/ --batch --stage 3
```

#### Training
```bash
# Train layout detection model
python ps05.py train --data data/train/ --output models/ --epochs 100
```

#### Evaluation
```bash
# Evaluate model performance
python ps05.py eval --predictions preds.json --ground-truth gt.json --output eval_results.json
```

#### Server
```bash
# Start API server
python ps05.py server --host 0.0.0.0 --port 8000
```

#### Submission Tools
```bash
# Create submission package
python ps05.py pack --input images/ --output submission/ --stage 3

# Generate overlay visualization
python ps05.py overlay --image image.png --json result.json --stage 3 --out overlay.png
```

## 📱 Mobile App Usage

### Features
- **Document Capture**: Camera, gallery, file picker
- **Processing Options**: Stage selection (1, 2, or 3)
- **Real-time Progress**: Processing status updates
- **Results Visualization**: Tabbed interface with detailed breakdowns
- **History Management**: Search, filter, export capabilities
- **Settings**: Server configuration and app preferences

### Navigation
- **Home Tab**: System status and quick actions
- **History Tab**: Previously processed documents
- **Settings Tab**: App configuration

### Processing Workflow
1. **Select Document**: Choose from camera, gallery, or files
2. **Choose Stage**: Select processing level (1, 2, or 3)
3. **Process**: Real-time progress tracking
4. **View Results**: Interactive results with tabs
5. **Share/Export**: Save or share results

## 🔧 Configuration

### Backend Configuration
Edit `configs/ps05_config.yaml`:
```yaml
system:
  name: "PS-05 Document Understanding System"
  version: "1.0.0"
  supported_languages: ["en", "hi", "ur", "ar", "ne", "fa"]

api:
  host: "0.0.0.0"
  port: 8000
  workers: 1

models:
  layout:
    model_path: "yolov8x.pt"
    confidence_threshold: 0.5
```

### Frontend Configuration
Edit `frontend/app.json`:
```json
{
  "expo": {
    "name": "PS-05 Document AI",
    "slug": "ps05-frontend",
    "version": "1.0.0",
    "orientation": "portrait",
    "platforms": ["ios", "android", "web"]
  }
}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Python Import Errors
```bash
# Solution: Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

#### 2. Node.js Dependency Issues
```bash
# Solution: Use legacy peer deps
npm install --legacy-peer-deps
```

#### 3. Polyglot Installation Error (Windows)
```bash
# Error: UnicodeDecodeError: 'charmap' codec can't decode byte
# Solution: Polyglot is optional and commented out in requirements.txt
# The system works without polyglot - it's used for additional language detection
# If you need polyglot, try installing it manually:
pip install polyglot --no-deps
# Or use an alternative language detection library
```

#### 4. CUDA/GPU Issues
```bash
# Solution: Install CPU-only version
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

#### 5. Port Already in Use
```bash
# Solution: Use different port
python ps05.py server --port 8001
```

#### 6. Memory Issues
```bash
# Solution: Reduce batch size in config
models:
  layout:
    batch_size: 1
```

### Performance Optimization

#### For GPU Users
```bash
# Install CUDA version
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

#### For Production
```bash
# Use multiple workers
python ps05.py server --workers 4

# Enable production mode
export ENVIRONMENT=production
```

### Logging and Debugging

#### Enable Debug Logging
```bash
# Set environment variable
export LOG_LEVEL=DEBUG
python ps05.py server
```

#### View Logs
```bash
# Check application logs
tail -f logs/ps05.log
```

## 📈 Performance Metrics

### Expected Performance (A100 GPU)
- **Stage 1**: ~400ms per page
- **Stage 2**: ~1.2s per page
- **Stage 3**: ~1.5s per page
- **Memory**: < 28GB VRAM

### Expected Performance (CPU)
- **Stage 1**: ~2s per page
- **Stage 2**: ~5s per page
- **Stage 3**: ~6s per page
- **Memory**: < 8GB RAM

## 🔄 Development Workflow

### 1. Backend Development
```bash
# Run tests
pytest tests/

# Format code
black src/
isort src/

# Lint code
flake8 src/
```

### 2. Frontend Development
```bash
cd frontend

# Run tests
npm test

# Lint code
npm run lint

# Type check
npx tsc --noEmit
```

### 3. Docker Development
```bash
# Build image
docker build -t ps05-system .

# Run container
docker run -p 8000:8000 ps05-system
```

## 📚 Additional Resources

### Documentation
- [PS-05 Challenge Details](README.md)
- [API Documentation](http://localhost:8000/docs)
- [Frontend README](frontend/README.md)

### Examples
- [Demo Script](demo.py)
- [Test Files](tests/)
- [Sample Data](data/)

### Support
- Check [Troubleshooting](#troubleshooting) section
- Review logs in `logs/` directory
- Check system requirements

---

## 🎉 Quick Start Summary

1. **Setup Backend**: `pip install -r requirements.txt`
2. **Setup Frontend**: `cd frontend && npm install --legacy-peer-deps`
3. **Run Demo**: `python demo.py`
4. **Start Server**: `python ps05.py server`
5. **Start Mobile App**: `cd frontend && npm start`

**The system is now ready for document processing! 🚀** 