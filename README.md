# PS-05 Intelligent Multilingual Document Understanding System

A production-ready, multilingual, layout-aware document understanding system that meets PS-05 requirements across English, Hindi, Urdu, Arabic, Nepali, and Persian languages.

## 🚀 Features

### Core Capabilities
- **Layout Detection**: 6-class detection (Background, Text, Title, List, Table, Figure)
- **Multilingual OCR**: Support for 6 languages with mixed script handling
- **Language Identification**: Automatic language detection with confidence scoring
- **Natural Language Generation**: Descriptions for tables, charts, maps, and images
- **JSON Output**: Structured output with bounding boxes and metadata

### Supported Languages
- **English (en)**: Latin script
- **Hindi (hi)**: Devanagari script  
- **Urdu (ur)**: Arabic script with Urdu-specific characters
- **Arabic (ar)**: Arabic script
- **Nepali (ne)**: Devanagari script with Nepali-specific characters
- **Persian (fa)**: Arabic script with Persian-specific characters

### Processing Stages
- **Stage 1**: Layout detection with mAP ≥0.5 IoU
- **Stage 2**: + OCR and language identification
- **Stage 3**: + Natural language descriptions for complex elements

## 📂 Project Structure

```
ps05/
├── configs/                 # Configuration files
│   └── ps05_config.yaml    # Main system configuration
├── src/                    # Core source code
│   ├── models/             # Model implementations
│   │   ├── layout_detector.py
│   │   ├── ocr_engine.py
│   │   ├── langid_classifier.py
│   │   └── nl_generator.py
│   ├── pipeline/           # Main processing pipeline
│   │   └── infer_page.py
│   ├── evaluation/         # Evaluation modules
│   │   └── layout_evaluator.py
│   └── data/              # Data preprocessing
│       └── preprocess.py
├── backend/               # API server
│   └── app/
│       ├── main.py
│       └── controllers/
├── scripts/               # Training and utility scripts
│   └── train_layout.py
├── tests/                 # Test files
├── data/                  # Data directories
├── models/                # Trained models
├── outputs/               # Output results
├── ps05.py               # Main CLI interface
└── requirements.txt      # Dependencies
```

## 🏗️ **Architecture**

### **Backend (Python/FastAPI)**
- **Framework**: FastAPI with Uvicorn ASGI server
- **ML Models**: YOLOv8 (layout), EasyOCR (text), Transformers (NL generation)
- **Languages**: Python 3.9+
- **APIs**: RESTful endpoints for document processing

### **Frontend (React Native/Expo)**
- **Framework**: React Native with Expo SDK 53
- **UI Library**: React Native Paper (Material Design)
- **Navigation**: React Navigation v6
- **Language**: TypeScript 5.3.0
- **Platforms**: iOS, Android, Web

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd ps05
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify installation
```bash
python ps05.py --help
```

## 🏋️ Usage

### Command Line Interface

The system provides a comprehensive CLI through `ps05.py`:

#### Single Image Inference
```bash
# Stage 1: Layout detection only
python ps05.py infer --input image.png --output results/ --stage 1

# Stage 2: Layout + OCR + Language ID
python ps05.py infer --input image.png --output results/ --stage 2

# Stage 3: Full pipeline with NL generation
python ps05.py infer --input image.png --output results/ --stage 3
```

#### Batch Processing
```bash
# Process all images in a directory
python ps05.py infer --input data/images/ --output results/ --batch --stage 3
```

#### Model Training
```bash
# Train layout detection model
python ps05.py train --data data/train/ --output models/ --epochs 100 --validate
```

#### Evaluation
```bash
# Evaluate model performance
python ps05.py eval --predictions preds.json --ground-truth gt.json --output eval_results.json
```

#### API Server
```bash
# Start the FastAPI server
python ps05.py server --host 0.0.0.0 --port 8000
```

### API Usage

#### Start the server
```bash
python ps05.py server --port 8000
```

#### API Endpoints
- `POST /api/v1/infer`: Process document images
- `GET /api/v1/health`: Health check
- `GET /api/v1/info`: System information
- `GET /docs`: Interactive API documentation

#### Example API Request
```bash
curl -X POST "http://localhost:8000/api/v1/infer?stage=3" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.png"
```

## 📊 Output Format

### Stage 1 Output (Layout Detection)
```json
{
  "page": 1,
  "size": {"w": 2480, "h": 3508},
  "elements": [
    {"id": "e1", "cls": "Title", "bbox": [x, y, h, w], "score": 0.97},
    {"id": "e2", "cls": "Text", "bbox": [x, y, h, w], "score": 0.94},
    {"id": "e3", "cls": "Table", "bbox": [x, y, h, w], "score": 0.92},
    {"id": "e4", "cls": "Figure", "bbox": [x, y, h, w], "score": 0.90}
  ],
  "preprocess": {"deskew_angle": -2.1}
}
```

### Stage 2+ Output (Additional Fields)
```json
{
  "text_lines": [
    {"bbox": [x, y, h, w], "text": "...", "lang": "hi", "score": 0.96},
    {"bbox": [x, y, h, w], "text": "...", "lang": "ar", "dir": "rtl", "score": 0.95}
  ],
  "tables": [
    {"bbox": [x, y, h, w], "summary": "The table lists quarterly revenue...", "confidence": 0.89}
  ],
  "figures": [
    {"bbox": [x, y, h, w], "summary": "A photograph of...", "confidence": 0.87}
  ],
  "charts": [
    {"bbox": [x, y, h, w], "type": "bar", "summary": "A bar chart showing...", "confidence": 0.86}
  ],
  "maps": [
    {"bbox": [x, y, h, w], "summary": "A map of ... highlighting ...", "confidence": 0.84}
  ]
}
```

## 🧪 Evaluation Metrics

### Layout Detection
- **mAP**: Mean Average Precision at IoU thresholds
- **IoU**: Intersection over Union for bounding box accuracy
- **Precision/Recall/F1**: Per-class and overall metrics

### OCR Performance
- **CER**: Character Error Rate
- **WER**: Word Error Rate
- **Language-specific breakdowns**

### Language Identification
- **Accuracy**: Overall classification accuracy
- **Precision/Recall/F1**: Per-language metrics
- **Confusion matrix**: Cross-language analysis

### Natural Language Generation
- **BLEURT**: Semantic similarity scoring
- **BERTScore**: Contextual similarity
- **BLEU**: N-gram overlap metrics

## ⚡ Performance Targets

### Throughput
- **Layout Detection**: ≤ 400ms per 2480×3508 page on A100
- **Full Pipeline**: ≤ 1.5s with OCR and NL generation
- **Batch Processing**: 4-8 pages per batch

### Memory Usage
- **Stage 1**: < 12 GB VRAM
- **Full Pipeline**: < 28 GB VRAM
- **CPU Fallback**: Available for all components

### Accuracy Targets
- **Layout mAP**: ≥ 0.90 on internal validation
- **OCR CER**: < 5% for clean documents
- **Language ID**: > 95% accuracy for single-language documents

## 🔧 Configuration

The system is configured through `configs/ps05_config.yaml`:

```yaml
system:
  name: "PS-05 Document Understanding System"
  version: "1.0.0"
  stage: 1
  target_languages: ["en", "hi", "ur", "ar", "ne", "fa"]

models:
  layout:
    type: "yolo"
    backbone: "yolov8x"
    classes: ["Background", "Text", "Title", "List", "Table", "Figure"]
    confidence_threshold: 0.5

  ocr:
    type: "easyocr"
    languages: ["en", "hi", "ur", "ar", "ne", "fa"]
    gpu: true
```

## 🛠️ Development

### Running Tests
```bash
pytest tests/ --maxfail=1 --disable-warnings -q
```

### Code Quality
```bash
black src/ tests/
flake8 src/ tests/
mypy src/
```

### Adding New Languages
1. Update `configs/ps05_config.yaml` with new language codes
2. Add language-specific characters in `src/models/langid_classifier.py`
3. Update OCR engine configuration
4. Test with sample documents

## 📈 Training Pipeline

### Data Preparation
```bash
# Preprocess raw images
python src/data/preprocess.py --raw data/raw --out data/processed
```

### Model Training
```bash
# Train layout detector
python ps05.py train --data data/train/ --output models/ --epochs 100 --validate
```

### Evaluation
```bash
# Evaluate on test set
python ps05.py eval --predictions preds.json --ground-truth gt.json --output results.json
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
docker build -t ps05-system .

# Run container
docker run -p 8000:8000 -v /data:/app/data ps05-system
```

### Kubernetes Deployment
```bash
# Apply deployment
kubectl apply -f infra/k8s/deployment.yaml

# Check status
kubectl get pods -l app=ps05-system
```

## 📋 Roadmap

### Phase A (Current)
- [x] Core pipeline implementation
- [x] Layout detection with YOLOv8
- [x] Multilingual OCR with EasyOCR
- [x] Language identification
- [x] Basic NL generation

### Phase B (Next)
- [ ] Advanced table structure analysis
- [ ] Chart data extraction
- [ ] Map entity recognition
- [ ] Performance optimization

### Phase C (Future)
- [ ] Additional language support
- [ ] Advanced NL generation models
- [ ] Real-time processing capabilities
- [ ] Cloud deployment automation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

Apache 2.0 License

## 👥 Team

Maintained by the PS-05 Document Understanding Team.

---

**Note**: This system is designed for the PS-05 challenge requirements and supports production deployment with proper configuration and monitoring.
