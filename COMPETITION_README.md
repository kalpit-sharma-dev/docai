# PS-05: Intelligent Multilingual Document Understanding

## 🎯 Competition Overview

This repository contains the complete solution for **Problem Statement 5 (PS-05)** of the Intelligent Multilingual Document Understanding challenge.

### Stage 1: Document Layout Detection (Current Focus)
- **Objective**: Detect and classify document layout elements
- **Classes**: 6 layout classes (Background, Text, Title, List, Table, Figure)
- **Output**: JSON with bounding box coordinates `[x, y, w, h]` and class predictions
- **Evaluation**: mAP (Mean Average Precision) at IoU threshold >= 0.5

### Timeline
- **Mock Dataset**: Available from 15 Sep 2025
- **Shortlisting Dataset**: Released 4 Nov 2025
- **Solution Submission**: Due by 5 Nov 2025
- **Offline Evaluation**: Top 15-20 participants at IIT Delhi

## 🚀 Quick Start

### 1. Docker Deployment (Recommended for Competition)
```bash
# Build and run the complete system
docker-compose up --build

# Or run individual services
docker-compose up backend
docker-compose up frontend
```

### 2. Local Development
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

### 3. Stage 1 Testing
```bash
# Test the layout detection pipeline
python test_stage1.py

# Run inference on a single image
python ps05.py infer --input test_image.png --output results/ --stage 1

# Process batch of images
python ps05.py infer --input data/images/ --output results/ --batch --stage 1
```

## 📁 Repository Structure

```
docai/
├── backend/                 # FastAPI backend server
│   ├── app/                # Main application code
│   ├── deploy/             # Docker deployment files
│   └── requirements.txt    # Python dependencies
├── frontend/               # React Native mobile app
├── src/                    # Core ML pipeline code
│   ├── models/            # Layout detection models
│   ├── pipeline/          # Processing pipelines
│   └── evaluation/        # Evaluation metrics
├── scripts/                # Training and utility scripts
├── data/                   # Dataset storage
├── models/                 # Pre-trained models
├── tests/                  # Test suite
├── docs/                   # Documentation
├── ps05.py                # Main CLI interface
└── docker-compose.yml     # Complete system orchestration
```

## 🔧 System Requirements

### For Competition Evaluation
- **OS**: Ubuntu 24.04 LTS
- **CPU**: 48+ cores
- **RAM**: 256+ GB
- **GPU**: A-100, 40/80 GB
- **Time**: 2 hours for solution demonstration

### For Development
- **OS**: Windows 10/11, macOS, or Ubuntu 20.04+
- **Python**: 3.8-3.10
- **Node.js**: 16.x+
- **Memory**: 8GB RAM minimum (16GB recommended)

## 📊 Stage 1 Implementation Status

✅ **COMPLETED** - Ready for competition evaluation

### What's Implemented
1. **Layout Detection Model**: YOLOv8-based detector for 6 layout classes
2. **Training Pipeline**: Complete training workflow with validation
3. **Evaluation**: mAP calculation at IoU threshold >= 0.5
4. **Inference Pipeline**: Ready-to-use layout detection
5. **Docker Deployment**: Production-ready containerization
6. **API Interface**: RESTful API for document processing
7. **Mobile App**: React Native frontend for document capture

## 🎯 Competition Submission

### Required Output Format
```json
{
  "image_id": "document_001",
  "predictions": [
    {
      "bbox": [x, y, w, h],
      "class": 1,
      "class_name": "Text",
      "confidence": 0.95
    }
  ],
  "processing_time": 1.23
}
```

### Evaluation Metrics
- **mAP Score**: 100% weight for classification and localization
- **Robustness**: Solution execution time and memory footprint
- **Approach**: Methodology and architecture presentation

## 📚 Documentation

- [Stage 1 README](STAGE1_README.md) - Complete Stage 1 implementation details
- [Setup & Run Guide](SETUP_AND_RUN.md) - Detailed setup instructions
- [Execution Guide](EXECUTION_GUIDE.md) - How to run the system
- [API Documentation](docs/API/) - Backend API reference
- [Training Guide](docs/STAGES/) - Model training instructions

## 🤝 Support

For competition-related questions:
- **Mock Dataset**: Available from 15 Sep 2025
- **Mentor Sessions**: Available from 15 Aug 2025
- **Website Updates**: Check regularly for competition updates

## 📄 License

This project is developed for the PS-05 Intelligent Multilingual Document Understanding challenge.
