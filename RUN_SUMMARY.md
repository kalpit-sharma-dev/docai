# PS-05 Document Understanding System - Run Summary

## 🎯 Quick Start (5 Steps)

### 1. Automated Setup (Recommended)
```bash
# Linux/macOS
./quick_start.sh

# Windows
quick_start.bat
```

### 2. Manual Setup
```bash
# Backend
pip install -r requirements.txt
python ps05.py --help

# Frontend
cd frontend
npm install --legacy-peer-deps
```

### 3. Run Demo
```bash
python demo.py
```

### 4. Start API Server
```bash
python ps05.py server
```

### 5. Start Mobile App
```bash
cd frontend
npm start
```

## 📋 System Components

### Backend (Python/FastAPI)
- **Layout Detection**: YOLOv8 with 6 classes
- **OCR Engine**: EasyOCR with 6 languages
- **Language ID**: Script-based + ML classification
- **NL Generation**: Transformer-based text generation
- **API**: RESTful endpoints with documentation

### Frontend (React Native/Expo)
- **Mobile App**: Cross-platform (iOS, Android, Web)
- **5 Screens**: Home, Document, Results, History, Settings
- **Real-time Processing**: Progress tracking and status updates
- **Results Visualization**: Interactive tabbed interface

### CLI Tools
- **Inference**: Single/batch document processing
- **Training**: Model training and validation
- **Evaluation**: Performance metrics calculation
- **Submission**: Challenge submission packaging
- **Visualization**: Overlay image generation

## 🚀 Available Commands

### Main CLI Tool
```bash
python ps05.py [command] [options]
```

### Commands Overview
| Command | Description | Example |
|---------|-------------|---------|
| `infer` | Process documents | `python ps05.py infer --input doc.png --stage 3` |
| `train` | Train models | `python ps05.py train --data data/ --epochs 100` |
| `eval` | Evaluate performance | `python ps05.py eval --predictions pred.json` |
| `server` | Start API server | `python ps05.py server --port 8000` |
| `pack` | Create submission | `python ps05.py pack --input images/ --stage 3` |
| `overlay` | Generate visualization | `python ps05.py overlay --image doc.png --json result.json` |

### API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/info` | GET | System information |
| `/api/v1/infer` | POST | Process document |

### Frontend Commands
```bash
cd frontend
npm start          # Start development server
npm run android    # Run on Android
npm run ios        # Run on iOS (macOS only)
npm run web        # Run on web
```

## 📊 Processing Stages

### Stage 1: Layout Detection
- **Classes**: Background, Text, Title, List, Table, Figure
- **Output**: Bounding boxes with confidence scores
- **Performance**: ~400ms per page (GPU), ~2s per page (CPU)

### Stage 2: Layout + OCR + Language ID
- **Features**: Text extraction, language identification
- **Languages**: English, Hindi, Urdu, Arabic, Nepali, Persian
- **Output**: Text lines with bboxes and language codes
- **Performance**: ~1.2s per page (GPU), ~5s per page (CPU)

### Stage 3: Full Analysis
- **Features**: NL generation for complex elements
- **Elements**: Tables, charts, maps, images
- **Output**: Natural language descriptions
- **Performance**: ~1.5s per page (GPU), ~6s per page (CPU)

## 📁 Output Format

### JSON Structure
```json
{
  "page": 1,
  "size": {"w": 2480, "h": 3508},
  "elements": [
    {"id": "e1", "cls": "Title", "bbox": [x,y,w,h], "score": 0.97}
  ],
  "text_lines": [
    {"bbox": [x,y,w,h], "text": "...", "lang": "en", "score": 0.96}
  ],
  "tables": [
    {"bbox": [x,y,w,h], "summary": "...", "confidence": 0.89}
  ],
  "figures": [
    {"bbox": [x,y,w,h], "summary": "...", "confidence": 0.87}
  ],
  "charts": [
    {"bbox": [x,y,w,h], "type": "bar", "summary": "...", "confidence": 0.86}
  ],
  "maps": [
    {"bbox": [x,y,w,h], "summary": "...", "confidence": 0.84}
  ]
}
```

## 🔧 Configuration

### Backend Config (`configs/ps05_config.yaml`)
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

### Frontend Config (`frontend/app.json`)
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

## 🐳 Docker Deployment

### Build and Run
```bash
# Build image
docker build -t ps05-system .

# Run container
docker run -p 8000:8000 ps05-system

# Access API
curl http://localhost:8000/api/v1/health
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

## 🐛 Common Issues & Solutions

### Python Import Errors
```bash
# Solution: Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### Node.js Dependency Issues
```bash
# Solution: Use legacy peer deps
npm install --legacy-peer-deps
```

### CUDA/GPU Issues
```bash
# Solution: Install CPU-only version
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Port Already in Use
```bash
# Solution: Use different port
python ps05.py server --port 8001
```

## 📚 Documentation Files

| File | Description |
|------|-------------|
| `SETUP_AND_RUN.md` | Comprehensive setup and run guide |
| `COMMANDS.md` | Complete command reference |
| `README.md` | Project overview and details |
| `frontend/README.md` | Frontend-specific documentation |

## 🎯 Use Cases

### 1. Document Processing
```bash
# Process single document
python ps05.py infer --input document.png --output results/ --stage 3
```

### 2. Batch Processing
```bash
# Process multiple documents
python ps05.py infer --input documents/ --output results/ --batch --stage 3
```

### 3. API Integration
```bash
# Start server
python ps05.py server

# Process via API
curl -X POST "http://localhost:8000/api/v1/infer?stage=3" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.png"
```

### 4. Mobile App
```bash
# Start mobile app
cd frontend && npm start
# Scan QR code with Expo Go app
```

### 5. Challenge Submission
```bash
# Create submission package
python ps05.py pack --input images/ --output submission/ --stage 3

# Generate overlay for QA
python ps05.py overlay --image doc.png --json result.json --stage 3 --out overlay.png
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

## 📞 Support

### Getting Help
1. Check [Troubleshooting](#-common-issues--solutions) section
2. Review logs in `logs/` directory
3. Check system requirements
4. Run demo script: `python demo.py`

### System Status
```bash
# Check backend health
curl http://localhost:8000/api/v1/health

# Check system info
curl http://localhost:8000/api/v1/info

# Run tests
pytest tests/
```

---

## 🎉 Success Indicators

✅ **System is ready when:**
- `python ps05.py --help` shows all commands
- `python demo.py` completes successfully
- `python ps05.py server` starts without errors
- `cd frontend && npm start` shows QR code
- API endpoints respond correctly

**The PS-05 Document Understanding System is now fully operational! 🚀** 