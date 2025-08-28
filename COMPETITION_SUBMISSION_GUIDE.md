# PS-05 Competition Submission Guide

## 🎯 Competition Overview

This guide explains how to deploy and use the PS-05 Document Understanding System for the **Intelligent Multilingual Document Understanding Challenge**.

### Stage 1 Requirements
- **Objective**: Document Layout Detection
- **Classes**: 6 layout classes (Background, Text, Title, List, Table, Figure)
- **Output**: JSON with bounding box coordinates `[x, y, w, h]`
- **Evaluation**: mAP (Mean Average Precision) at IoU threshold >= 0.5
- **Weight**: 100% for classification and localization

### Timeline
- **Mock Dataset**: Available from 15 Sep 2025
- **Shortlisting Dataset**: Released 4 Nov 2025
- **Solution Submission**: Due by 5 Nov 2025
- **Offline Evaluation**: Top 15-20 participants at IIT Delhi

## 🚀 Quick Deployment

### Option 1: Automated Deployment (Recommended)
```bash
# Linux/macOS
chmod +x deploy_competition.sh
./deploy_competition.sh

# Windows
deploy_competition.bat
```

### Option 2: Manual Docker Deployment
```bash
# Build and start all services
docker-compose up --build -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### Option 3: Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app/main.py

# Frontend
cd frontend
npm install
npm start
```

## 🔧 System Verification

### 1. Health Check
```bash
# Backend health
curl http://localhost:8000/api/v1/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-01-XX...",
  "version": "1.0.0",
  "stage": 1
}
```

### 2. Stage 1 Test
```bash
# Run the Stage 1 test suite
python test_stage1.py

# Expected output:
# ✅ Stage 1 Layout Detection Test PASSED
# ✅ Model loading successful
# ✅ Inference pipeline working
# ✅ Output format validation passed
```

### 3. API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## 📊 Competition Evaluation

### 1. Input Format
The system accepts document images in the following formats:
- **Formats**: JPG, JPEG, PNG, BMP, TIFF
- **Size**: Up to 50MB per image
- **Content**: Documents may be rotated, blurred, or noisy

### 2. Output Format
```json
{
  "image_id": "document_001",
  "predictions": [
    {
      "bbox": [x, y, w, h],
      "class": 1,
      "class_name": "Text",
      "confidence": 0.95
    },
    {
      "bbox": [x, y, w, h],
      "class": 4,
      "class_name": "Table",
      "confidence": 0.92
    }
  ],
  "processing_time": 1.23,
  "image_size": [800, 600],
  "preprocessing": {
    "deskew_angle": -2.1,
    "denoised": true
  }
}
```

### 3. Class Definitions
| Class ID | Class Name | Description |
|----------|------------|-------------|
| 0 | Background | Empty/background areas |
| 1 | Text | Regular text paragraphs |
| 2 | Title | Document titles and headings |
| 3 | List | Bulleted/numbered lists |
| 4 | Table | Tabular data structures |
| 5 | Figure | Images, charts, diagrams |

## 🧪 Testing Your System

### 1. Single Image Test
```bash
# Process a single document image
python ps05.py infer \
  --input tests/test_data/test_document.png \
  --output results/ \
  --stage 1
```

### 2. Batch Processing Test
```bash
# Process multiple images
python ps05.py infer \
  --input data/test_images/ \
  --output results/ \
  --batch \
  --stage 1
```

### 3. Performance Test
```bash
# Run performance evaluation
python src/evaluation/stage1_evaluator.py \
  --predictions results/predictions.json \
  --ground-truth data/ground_truth.json \
  --output evaluation_results.json
```

## 📈 Performance Metrics

### 1. Layout Detection Accuracy
- **mAP@0.5**: Primary evaluation metric
- **mAP@0.75**: Secondary metric for high precision
- **Per-class metrics**: Precision, Recall, F1-score for each class

### 2. Processing Performance
- **Inference time**: Target < 1 second per image
- **Memory usage**: Target < 16GB VRAM
- **Throughput**: Target > 10 images per minute

### 3. System Reliability
- **Uptime**: 99.9% availability during evaluation
- **Error handling**: Graceful degradation on failures
- **Resource utilization**: Efficient CPU/GPU usage

## 🔍 Competition Demo Preparation

### 1. System Requirements Verification
```bash
# Check system specifications
python -c "
import psutil
import torch
print(f'CPU Cores: {psutil.cpu_count()}')
print(f'RAM: {psutil.virtual_memory().total / (1024**3):.1f} GB')
print(f'GPU Available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU Memory: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.1f} GB')
"
```

### 2. Model Performance Validation
```bash
# Validate model performance
python scripts/validate_model.py \
  --model models/layout_detector.pt \
  --test_data data/validation/ \
  --output validation_results.json
```

### 3. Demo Script Preparation
```bash
# Create demo script
cat > demo_competition.sh << 'EOF'
#!/bin/bash
echo "PS-05 Competition Demo Starting..."
echo "=================================="

# 1. System health check
echo "1. Checking system health..."
curl -s http://localhost:8000/api/v1/health | jq '.'

# 2. Load test image
echo "2. Processing test document..."
python ps05.py infer --input demo_document.png --output demo_results/ --stage 1

# 3. Display results
echo "3. Results:"
cat demo_results/result.json | jq '.'

# 4. Performance metrics
echo "4. Performance metrics:"
python src/evaluation/performance_analyzer.py --results demo_results/

echo "Demo completed successfully!"
EOF

chmod +x demo_competition.sh
```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Docker Services Not Starting
```bash
# Check Docker status
docker system info

# Restart Docker services
docker-compose down
docker-compose up --build -d

# Check logs
docker-compose logs ps05-backend
```

#### 2. Model Loading Failures
```bash
# Verify model files
ls -la models/

# Check model compatibility
python -c "
import torch
model = torch.load('models/yolov8x.pt', map_location='cpu')
print('Model loaded successfully')
"
```

#### 3. API Connection Issues
```bash
# Check service ports
netstat -tulpn | grep :8000

# Test API connectivity
curl -v http://localhost:8000/api/v1/health

# Check firewall settings
sudo ufw status
```

#### 4. Performance Issues
```bash
# Monitor system resources
htop
nvidia-smi  # If using GPU

# Check Docker resource limits
docker stats

# Optimize Docker settings
# Edit /etc/docker/daemon.json
```

## 📋 Pre-Submission Checklist

### System Requirements ✅
- [ ] Docker and Docker Compose installed
- [ ] Python 3.8+ environment available
- [ ] Sufficient disk space (>10GB)
- [ ] Network connectivity for model downloads

### Functionality Tests ✅
- [ ] Stage 1 inference working
- [ ] JSON output format correct
- [ ] Bounding box coordinates valid
- [ ] Class predictions accurate
- [ ] Processing time acceptable

### Performance Validation ✅
- [ ] mAP@0.5 > 0.8 on validation set
- [ ] Inference time < 2 seconds per image
- [ ] Memory usage < 20GB
- [ ] System stable for 2+ hours

### Documentation Ready ✅
- [ ] README.md updated
- [ ] API documentation accessible
- [ ] Deployment instructions clear
- [ ] Troubleshooting guide available

## 🎯 Competition Day Preparation

### 1. System Backup
```bash
# Create system backup
tar -czf ps05_competition_backup_$(date +%Y%m%d).tar.gz \
  --exclude=venv \
  --exclude=__pycache__ \
  --exclude=*.pyc \
  .
```

### 2. Demo Environment Setup
```bash
# Prepare demo environment
mkdir -p competition_demo
cp -r tests/test_data competition_demo/
cp deploy_competition.sh competition_demo/
cp docker-compose.yml competition_demo/
cp -r configs competition_demo/
```

### 3. Quick Start Commands
```bash
# Competition day quick start
cd competition_demo
./deploy_competition.sh

# Verify system
curl http://localhost:8000/api/v1/health
python test_stage1.py
```

## 📞 Support and Resources

### Competition Resources
- **Official Website**: Check regularly for updates
- **Mentor Sessions**: Available from 15 Aug 2025
- **Mock Dataset**: Available from 15 Sep 2025
- **Leaderboard**: Published every Tuesday from 15 Sep

### Technical Support
- **Documentation**: This repository and linked guides
- **Issues**: GitHub issues for technical problems
- **Community**: PS-05 participant forums

### Evaluation Contact
- **Evaluation Date**: 4 November 2025
- **Location**: IIT Delhi
- **Duration**: 2 hours per participant
- **Resources**: A-100 GPU, 48+ cores, 256+ GB RAM

---

## 🏆 Good Luck!

Your PS-05 Document Understanding System is now ready for competition evaluation. Remember:

1. **Test thoroughly** before submission
2. **Document everything** clearly
3. **Prepare for offline evaluation** at IIT Delhi
4. **Meet the 5 November deadline**

**Best of luck in the PS-05 Challenge!** 🚀
