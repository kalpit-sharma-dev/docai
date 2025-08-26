# PS-05 Command Reference

## 🚀 Quick Start Commands

### Automated Setup
```bash
# Linux/macOS
./quick_start.sh

# Windows
quick_start.bat
```

### Manual Setup
```bash
# Backend
pip install -r requirements.txt
python ps05.py --help

# Frontend
cd frontend
npm install --legacy-peer-deps
npm start
```

## 🖥️ Backend Commands

### Main CLI Tool
```bash
python ps05.py [command] [options]
```

### Available Commands

#### 1. Inference (Process Documents)
```bash
# Single image
python ps05.py infer --input image.png --output results/ --stage 3

# Batch processing
python ps05.py infer --input images/ --output results/ --batch --stage 3

# Options:
# --input: Input image or directory
# --output: Output directory
# --stage: Processing stage (1, 2, or 3)
# --config: Configuration file path
# --batch: Enable batch processing mode
```

#### 2. Training
```bash
# Train layout detection model
python ps05.py train --data data/train/ --output models/ --epochs 100

# Options:
# --data: Training data directory
# --output: Output directory for models
# --epochs: Number of training epochs
# --batch-size: Batch size for training
# --validate: Run validation after training
```

#### 3. Evaluation
```bash
# Evaluate model performance
python ps05.py eval --predictions preds.json --ground-truth gt.json --output eval_results.json

# Options:
# --predictions: Predictions JSON file
# --ground-truth: Ground truth JSON file
# --output: Output results file
```

#### 4. Server (API)
```bash
# Start API server
python ps05.py server --host 0.0.0.0 --port 8000

# Options:
# --host: Server host (default: 0.0.0.0)
# --port: Server port (default: 8000)
# --reload: Enable auto-reload
# --workers: Number of workers (default: 1)
```

#### 5. Submission Tools
```bash
# Create submission package
python ps05.py pack --input images/ --output submission/ --stage 3

# Generate overlay visualization
python ps05.py overlay --image image.png --json result.json --stage 3 --out overlay.png

# Options:
# --input: Image file or directory
# --output: Output directory
# --stage: Processing stage (1, 2, or 3)
# --zip-name: Name of the zip file
# --config: Configuration file path
```

## 📱 Frontend Commands

### Development Server
```bash
cd frontend
npm start
```

### Platform-Specific Commands
```bash
# Android
npm run android

# iOS (macOS only)
npm run ios

# Web
npm run web
```

### Development Tools
```bash
# Run tests
npm test

# Lint code
npm run lint

# Type check
npx tsc --noEmit
```

## 🌐 API Commands

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### System Information
```bash
curl http://localhost:8000/api/v1/info
```

### Process Document
```bash
# Using curl
curl -X POST "http://localhost:8000/api/v1/infer?stage=3" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.png"

# Using Python
import requests
url = "http://localhost:8000/api/v1/infer"
files = {"file": open("document.png", "rb")}
params = {"stage": 3}
response = requests.post(url, files=files, params=params)
result = response.json()
```

## 🐳 Docker Commands

### Build Image
```bash
docker build -t ps05-system .
```

### Run Container
```bash
docker run -p 8000:8000 ps05-system
```

### Development with Docker
```bash
# Build with development dependencies
docker build -t ps05-dev --target development .

# Run with volume mounting
docker run -p 8000:8000 -v $(pwd):/app ps05-dev
```

## 🔧 Utility Commands

### Demo Script
```bash
# Run complete demo
python demo.py
```

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_ps05_pipeline.py

# Run with coverage
pytest --cov=src tests/
```

### Code Quality
```bash
# Format code
black src/
isort src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## 📊 Monitoring Commands

### Performance Monitoring
```bash
# Check system resources
htop
nvidia-smi  # If using GPU

# Monitor API server
curl http://localhost:8000/api/v1/health
```

### Logs
```bash
# View application logs
tail -f logs/ps05.log

# View server logs
python ps05.py server --log-level debug
```

## 🚨 Troubleshooting Commands

### Common Issues
```bash
# Check Python environment
python --version
pip list

# Check Node.js environment
node --version
npm list

# Check GPU availability
python -c "import torch; print(torch.cuda.is_available())"

# Check model files
ls -la *.pt
ls -la models/
```

### Reset Environment
```bash
# Remove virtual environment
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Clear frontend cache
cd frontend
rm -rf node_modules/
npm install --legacy-peer-deps
```

## 📈 Performance Commands

### Benchmark
```bash
# Single image benchmark
time python ps05.py infer --input test.png --output results/ --stage 3

# Batch benchmark
time python ps05.py infer --input test_images/ --output results/ --batch --stage 3
```

### Memory Usage
```bash
# Monitor memory usage
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"
```

## 🔄 Development Workflow

### Daily Development
```bash
# 1. Start backend server
python ps05.py server --reload

# 2. Start frontend (in another terminal)
cd frontend && npm start

# 3. Run tests
pytest tests/

# 4. Check code quality
black src/
flake8 src/
```

### Production Deployment
```bash
# 1. Build Docker image
docker build -t ps05-production .

# 2. Run with production settings
docker run -p 8000:8000 -e ENVIRONMENT=production ps05-production

# 3. Monitor
curl http://localhost:8000/api/v1/health
```

---

## 📝 Command Examples

### Complete Workflow Example
```bash
# 1. Setup
./quick_start.sh

# 2. Start server
python ps05.py server

# 3. Process document
python ps05.py infer --input document.png --output results/ --stage 3

# 4. Create submission
python ps05.py pack --input document.png --output submission/ --stage 3

# 5. Generate overlay
python ps05.py overlay --image document.png --json results/result.json --stage 3 --out overlay.png
```

### API Workflow Example
```bash
# 1. Start server
python ps05.py server

# 2. Check health
curl http://localhost:8000/api/v1/health

# 3. Process document
curl -X POST "http://localhost:8000/api/v1/infer?stage=3" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.png"

# 4. View results
cat response.json
``` 