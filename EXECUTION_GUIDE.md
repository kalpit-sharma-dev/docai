# PS-05: Intelligent Multilingual Document Understanding
## Complete Execution Guide

This document provides a step-by-step guide to run all components of the PS-05 project across all three stages.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Stage 1: Document Layout Detection](#stage-1-document-layout-detection)
4. [Stage 2: OCR and Language Detection](#stage-2-ocr-and-language-detection)
5. [Stage 3: Natural Language Generation](#stage-3-natural-language-generation)
6. [Complete Pipeline Execution](#complete-pipeline-execution)
7. [Testing and Validation](#testing-and-validation)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- Python 3.8+ (3.10+ recommended)
- 8GB+ RAM (16GB+ recommended for training)
- 4GB+ GPU memory (for CUDA acceleration)
- 10GB+ free disk space

### Software Dependencies
- Git
- Docker (optional, for containerized deployment)
- CUDA toolkit (optional, for GPU acceleration)

## Environment Setup

### Step 1: Clone and Navigate to Project
```bash
cd /d/IIT/docai
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download Pre-trained Models
```bash
# Create models directory
mkdir -p models/easyocr
mkdir -p models/transformers

# Download YOLOv8 model (if not already present)
python -c "from ultralytics import YOLO; YOLO('yolov8x.pt')"

# Download EasyOCR models (will be downloaded automatically on first use)
python -c "import easyocr; easyocr.Reader(['en'])"
```

## Stage 1: Document Layout Detection

### Step 1: Data Preparation
```bash
# Navigate to data directory
cd data

# Check training data structure
ls -la train/
ls -la processed/

# Return to root
cd ..
```

### Step 2: Run EDA (Exploratory Data Analysis)
```bash
# Run EDA notebook
jupyter notebook notebooks/eda.ipynb

# Or run EDA script directly
python -c "
import pandas as pd
import matplotlib.pyplot as plt
from src.data.preprocess import analyze_dataset
analyze_dataset('data/train')
"
```

### Step 3: Train Layout Detection Model
```bash
# Train YOLOv8 model on custom dataset
python scripts/train.py

# Or use the layout training script
python src/layout/train.py
```

### Step 4: Test Layout Detection
```bash
# Test on sample images
python -c "
from src.models.layout_detector import LayoutDetector
detector = LayoutDetector('models/best.pt')
result = detector.detect('data/train/sample.jpg')
print(result)
"
```

### Step 5: Run Complete Stage 1 Pipeline
```bash
# Process single document
python -c "
from src.pipeline.infer_page import process_document
result = process_document('data/train/sample.jpg')
print(result)
"

# Process multiple documents
python -c "
from src.pipeline.infer_page import batch_process
results = batch_process('data/train/')
print(f'Processed {len(results)} documents')
"
```

## Stage 2: OCR and Language Detection

### Step 1: Test Individual Components
```bash
# Test Multilingual OCR
python -c "
from src.ocr.multilingual_ocr import MultilingualOCR
ocr = MultilingualOCR()
result = ocr.extract_text('data/train/sample.jpg')
print('OCR Result:', result)
"

# Test Language Detection
python -c "
from src.ocr.language_detector import LanguageDetector
detector = LanguageDetector()
result = detector.detect_language('Hello World')
print('Language:', result)
"

# Test Visual to Text Generation
python -c "
from src.nlg.visual_to_text import VisualToTextGenerator
generator = VisualToTextGenerator()
result = generator.generate_description('data/train/sample.jpg', 'table')
print('Generated Text:', result)
"
```

### Step 2: Run Stage 2 Pipeline
```bash
# Process single document with Stage 2
python -c "
from src.pipeline.stage2_pipeline import Stage2Pipeline
pipeline = Stage2Pipeline()
result = pipeline.process_document('data/train/sample.jpg')
print('Stage 2 Result:', result)
"

# Batch process with Stage 2
python -c "
from src.pipeline.stage2_pipeline import Stage2Pipeline
pipeline = Stage2Pipeline()
results = pipeline.batch_process('data/train/')
print(f'Stage 2 processed {len(results)} documents')
"
```

### Step 3: Evaluate Stage 2 Performance
```bash
# Run evaluation
python -c "
from src.pipeline.stage2_pipeline import Stage2Pipeline
pipeline = Stage2Pipeline()
metrics = pipeline.evaluate_performance('data/train/')
print('Stage 2 Metrics:', metrics)
"
```

## Stage 3: Natural Language Generation

### Step 1: Test Stage 3 Components
```bash
# Test enhanced visual generation
python -c "
from src.nlg.visual_to_text import VisualToTextGenerator
generator = VisualToTextGenerator()
result = generator.generate_description('data/train/sample.jpg', 'chart', enhanced=True)
print('Enhanced Description:', result)
"
```

### Step 2: Run Stage 3 Pipeline
```bash
# Process single document with Stage 3
python -c "
from src.pipeline.stage3_pipeline import Stage3Pipeline
pipeline = Stage3Pipeline()
result = pipeline.process_document('data/train/sample.jpg')
print('Stage 3 Result:', result)
"

# Batch process with Stage 3
python -c "
from src.pipeline.stage3_pipeline import Stage3Pipeline
pipeline = Stage3Pipeline()
results = pipeline.batch_process('data/train/')
print(f'Stage 3 processed {len(results)} documents')
"
```

### Step 3: Evaluate Stage 3 Performance
```bash
# Run Stage 3 evaluation
python -c "
from src.pipeline.stage3_pipeline import Stage3Pipeline
pipeline = Stage3Pipeline()
metrics = pipeline.evaluate_stage3_performance('data/train/')
print('Stage 3 Metrics:', metrics)
"
```

## Complete Pipeline Execution

### Option 1: Run All Stages Sequentially
```bash
# Create a comprehensive execution script
python -c "
import os
from src.pipeline.stage1_pipeline import Stage1Pipeline
from src.pipeline.stage2_pipeline import Stage2Pipeline
from src.pipeline.stage3_pipeline import Stage3Pipeline

# Initialize pipelines
stage1 = Stage1Pipeline()
stage2 = Stage2Pipeline()
stage3 = Stage3Pipeline()

# Process document through all stages
doc_path = 'data/train/sample.jpg'

print('=== STAGE 1: Layout Detection ===')
stage1_result = stage1.process_document(doc_path)
print('Stage 1 completed')

print('=== STAGE 2: OCR and Language Detection ===')
stage2_result = stage2.process_document(doc_path)
print('Stage 2 completed')

print('=== STAGE 3: Natural Language Generation ===')
stage3_result = stage3.process_document(doc_path)
print('Stage 3 completed')

print('=== ALL STAGES COMPLETED ===')
"
```

### Option 2: Use Demo Script
```bash
# Run the main demo script
python demo.py

# Or run specific demo functions
python -c "
from demo import run_stage1_demo, run_stage2_demo, run_stage3_demo

print('Running Stage 1 Demo...')
run_stage1_demo()

print('Running Stage 2 Demo...')
run_stage2_demo()

print('Running Stage 3 Demo...')
run_stage3_demo()
"
```

## Testing and Validation

### Step 1: Run Unit Tests
```bash
# Run basic tests
python -m pytest tests/test_basic.py -v

# Run document tests
python -m pytest tests/test_doc.py -v

# Run smoke tests
python -m pytest tests/smoke_test.py -v
```

### Step 2: Run Stage 2 & 3 Tests
```bash
# Run comprehensive Stage 2 & 3 tests
python test_stage2_stage3.py
```

### Step 3: Run Pipeline Tests
```bash
# Test PS-05 pipeline
python -m pytest tests/test_ps05_pipeline.py -v
```

### Step 4: Validate Results
```bash
# Check output directories
ls -la demo_output/
ls -la data/processed/

# Validate JSON outputs
python -c "
import json
import os

# Check Stage 1 results
if os.path.exists('demo_output/stage1_results.json'):
    with open('demo_output/stage1_results.json', 'r') as f:
        data = json.load(f)
    print('Stage 1 results:', len(data), 'documents processed')

# Check Stage 2 results
if os.path.exists('demo_output/stage2_results.json'):
    with open('demo_output/stage2_results.json', 'r') as f:
        data = json.load(f)
    print('Stage 2 results:', len(data), 'documents processed')

# Check Stage 3 results
if os.path.exists('demo_output/stage3_results.json'):
    with open('demo_output/stage3_results.json', 'r') as f:
        data = json.load(f)
    print('Stage 3 results:', len(data), 'documents processed')
"
```

## Quick Start Commands

### For Development/Testing
```bash
# Quick setup and test
python quick_start.bat  # Windows
./quick_start.sh        # Linux/Mac

# Or manually:
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
pip install -r requirements.txt
python test_stage2_stage3.py
```

### For Production/Deployment
```bash
# Using Docker
docker-compose up -d

# Or direct execution
python run.py
```

### For Training
```bash
# Train layout detection model
python scripts/train.py

# Train OCR models (if needed)
python src/ocr/recog/train.py
```

## File Execution Sequence Summary

### Setup Phase (One-time)
1. **Environment Setup**: `venv\Scripts\activate` + `pip install -r requirements.txt`
2. **Model Download**: Automatic on first use, or manual download

### Development Phase
1. **Data Preparation**: Check `data/train/` structure
2. **EDA**: Run `notebooks/eda.ipynb`
3. **Training**: Run `scripts/train.py` (if needed)

### Testing Phase
1. **Unit Tests**: `python -m pytest tests/`
2. **Component Tests**: `python test_stage2_stage3.py`
3. **Pipeline Tests**: `python -m pytest tests/test_ps05_pipeline.py`

### Execution Phase
1. **Stage 1**: Layout detection via `src/pipeline/infer_page.py`
2. **Stage 2**: OCR + Language detection via `src/pipeline/stage2_pipeline.py`
3. **Stage 3**: NLG via `src/pipeline/stage3_pipeline.py`

### Validation Phase
1. **Check Outputs**: Verify `demo_output/` and `data/processed/`
2. **Validate JSON**: Check format and content of results
3. **Performance Metrics**: Run evaluation functions

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: CUDA/GPU Not Available
```bash
# Check CUDA availability
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# Force CPU usage
export CUDA_VISIBLE_DEVICES=""
# or
set CUDA_VISIBLE_DEVICES=""  # Windows
```

#### Issue 2: Model Download Failures
```bash
# Manual model download
python -c "
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-medium')
model = AutoModel.from_pretrained('microsoft/DialoGPT-medium')
"
```

#### Issue 3: Memory Issues
```bash
# Reduce batch size in training
python scripts/train.py --batch-size 4

# Use gradient accumulation
python scripts/train.py --accumulate 4
```

#### Issue 4: File Format Support
```bash
# Check supported formats
python -c "
from src.services.file_manager import FileManager
fm = FileManager()
print('Supported formats:', fm.supported_formats)
"
```

### Performance Optimization

#### For Training
```bash
# Use mixed precision
python scripts/train.py --amp

# Use gradient checkpointing
python scripts/train.py --gradient-checkpointing

# Use distributed training
python -m torch.distributed.launch scripts/train.py
```

#### For Inference
```bash
# Enable model caching
export TRANSFORMERS_CACHE="/path/to/cache"

# Use model quantization
python -c "
from src.models.layout_detector import LayoutDetector
detector = LayoutDetector('models/best.pt', quantized=True)
"
```

## Monitoring and Logging

### Enable Debug Logging
```bash
# Set log level
export LOG_LEVEL=DEBUG
# or
set LOG_LEVEL=DEBUG  # Windows

# Run with verbose output
python -u run.py --verbose
```

### Performance Monitoring
```bash
# Monitor GPU usage
nvidia-smi

# Monitor memory usage
python -c "
import psutil
print('Memory usage:', psutil.virtual_memory().percent, '%')
print('CPU usage:', psutil.cpu_percent(), '%')
"
```

## Conclusion

This execution guide provides a comprehensive roadmap for running all components of the PS-05 project. Follow the sequence outlined above to ensure proper setup, testing, and execution of all stages.

### Key Success Factors
1. **Follow the sequence**: Setup → Development → Testing → Execution → Validation
2. **Verify each stage**: Ensure each stage completes successfully before proceeding
3. **Monitor resources**: Watch memory, GPU, and disk usage during execution
4. **Validate outputs**: Check JSON format and content quality at each stage
5. **Use appropriate models**: Ensure pre-trained models are downloaded and accessible

### Support
- Check `README.md` for general project information
- Check `STAGE2_STAGE3_README.md` for detailed Stage 2 & 3 information
- Check `STAGE2_STAGE3_COMPLETION_SUMMARY.md` for implementation details
- Check `ERRORS_FIXED.md` for common issues and solutions

Happy coding! 🚀
