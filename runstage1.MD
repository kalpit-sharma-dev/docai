I'll document all the commands that were run for Stage 1 so you can easily reproduce them in the future. Here's the complete command documentation:

## **📋 COMPLETE STAGE 1 COMMAND DOCUMENTATION**

### **1. Environment Setup & GPU Configuration**

```bash
# Navigate to project directory
cd /d/IIT/docai

# Create virtual environment
python -m venv ps05_env

# Activate virtual environment (Windows)
source ps05_env/Scripts/activate

# Install GPU-enabled PyTorch for RTX 2070
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other required dependencies
pip install ultralytics opencv-python PyMuPDF python-docx python-pptx tqdm pyyaml albumentations

# Install evaluation and processing dependencies
pip install easyocr pytesseract langdetect transformers pycocotools jiwer sacrebleu bert-score
```

### **2. GPU Verification**

```bash
# Verify RTX 2070 GPU availability
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('Device name:', torch.cuda.get_device_name(0)); print('CUDA version:', torch.version.cuda)"
```

### **3. Enhanced Data Preprocessing**

```bash
# Run comprehensive preprocessing on training dataset
python scripts/enhanced_preprocessing.py --input data/train --output data/enhanced_processed_complete
```

### **4. Dataset Preparation for YOLO Training**

```bash
# Convert annotations to YOLO format
python scripts/prepare_dataset.py --data data/enhanced_processed_complete --output data/yolo_enhanced_dataset
```

### **5. Stage 1 Training with GPU**

```bash
# Train layout detection model using GPU acceleration
python scripts/train_stage1.py --data data/enhanced_processed_complete --output outputs/stage1_enhanced --epochs 5 --batch-size 4 --create-submission
```

### **6. Model Testing & Validation**

```bash
# Test trained model on individual images
python ps05.py infer --input data/enhanced_processed_complete/images/doc_00000_processed.png --output results/stage1_test --stage 1

python ps05.py infer --input data/enhanced_processed_complete/images/doc_00001_processed.png --output results/stage1_test2 --stage 1

python ps05.py infer --input data/enhanced_processed_complete/images/doc_00002_processed.png --output results/stage1_test3 --stage 1
```

### **7. Batch Processing & Submission Creation**

```bash
# Create complete submission package
python scripts/pack_submission.py --input data/enhanced_processed_complete/images/ --output results/stage1_submission --stage 1 --zip-name stage1_submission.zip
```

### **8. Verification Commands**

```bash
# Check GPU status
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('Device name:', torch.cuda.get_device_name(0))"

# Check directory structures
ls -la data/enhanced_processed_complete/
ls -la data/yolo_enhanced_dataset/
ls -la outputs/stage1_enhanced/
ls -la results/stage1_submission/

# Count files
find data/enhanced_processed_complete/images -name "*.png" | wc -l
find data/enhanced_processed_complete/annotations -name "*.json" | wc -l
```

## **�� QUICK START SCRIPT**

Create a file called `run_stage1.sh` (or `run_stage1.bat` for Windows) with all commands:

```bash
#!/bin/bash
# run_stage1.sh - Complete Stage 1 execution script

echo "🚀 Starting PS-05 Stage 1 Pipeline..."

# 1. Environment Setup
echo "📦 Setting up environment..."
python -m venv ps05_env
source ps05_env/Scripts/activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install ultralytics opencv-python PyMuPDF python-docx python-pptx tqdm pyyaml albumentations
pip install easyocr pytesseract langdetect transformers pycocotools jiwer sacrebleu bert-score

# 2. GPU Verification
echo "�� Verifying GPU..."
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('Device name:', torch.cuda.get_device_name(0))"

# 3. Enhanced Preprocessing
echo "🔄 Running enhanced preprocessing..."
python scripts/enhanced_preprocessing.py --input data/train --output data/enhanced_processed_complete

# 4. Dataset Preparation
echo "📊 Preparing dataset..."
python scripts/prepare_dataset.py --data data/enhanced_processed_complete --output data/yolo_enhanced_dataset

# 5. Stage 1 Training
echo "🎯 Training Stage 1 model..."
python scripts/train_stage1.py --data data/enhanced_processed_complete --output outputs/stage1_enhanced --epochs 5 --batch-size 4 --create-submission

# 6. Test Model
echo "🧪 Testing trained model..."
python ps05.py infer --input data/enhanced_processed_complete/images/doc_00000_processed.png --output results/stage1_test --stage 1

# 7. Create Submission
echo "📦 Creating submission package..."
python scripts/pack_submission.py --input data/enhanced_processed_complete/images/ --output results/stage1_submission --stage 1 --zip-name stage1_submission.zip

echo "✅ Stage 1 Pipeline Complete!"
echo "📁 Results saved to: results/stage1_submission/"
echo "🎯 Trained model: outputs/stage1_enhanced/training/layout_detector3/weights/best.pt"
```

## **📁 OUTPUT DIRECTORY STRUCTURE**

After running all commands, you'll have this structure:

```
outputs/stage1_enhanced/          # Trained model outputs
├── training/layout_detector3/weights/
│   ├── best.pt                   # Best trained model
│   └── last.pt                   # Last checkpoint

data/enhanced_processed_complete/  # Preprocessed dataset
├── images/                        # Processed images
├── annotations/                   # Processed annotations
└── metadata/                      # Processing metadata

data/yolo_enhanced_dataset/        # YOLO format dataset
├── train/                         # Training data
├── val/                          # Validation data
├── test/                         # Test data
└── dataset.yaml                  # Dataset configuration

results/                          # Inference results
├── stage1_test/                  # Individual test results
├── stage1_test2/                 # Additional test results
├── stage1_test3/                 # More test results
└── stage1_submission/            # Final submission package
    ├── index.json                # Submission index
    ├── json/                     # All JSON results
    └── stage1_submission.zip     # Zipped submission
```

## **⚡ SINGLE COMMAND EXECUTION**

For quick execution, you can run this single command that executes the entire pipeline:

```bash
# Run complete Stage 1 pipeline in one command
python -c "
import subprocess
import sys

commands = [
    'python scripts/enhanced_preprocessing.py --input data/train --output data/enhanced_processed_complete',
    'python scripts/prepare_dataset.py --data data/enhanced_processed_complete --output data/yolo_enhanced_dataset',
    'python scripts/train_stage1.py --data data/enhanced_processed_complete --output outputs/stage1_enhanced --epochs 5 --batch-size 4 --create-submission',
    'python ps05.py infer --input data/enhanced_processed_complete/images/doc_00000_processed.png --output results/stage1_test --stage 1',
    'python scripts/pack_submission.py --input data/enhanced_processed_complete/images/ --output results/stage1_submission --stage 1 --zip-name stage1_submission.zip'
]

for cmd in commands:
    print(f'Running: {cmd}')
    subprocess.run(cmd, shell=True, check=True)
    print('Command completed successfully')

print('Stage 1 pipeline completed!')
"
```

## **🔧 TROUBLESHOOTING COMMANDS**

If you encounter issues, use these diagnostic commands:

```bash
# Check GPU status
nvidia-smi

# Check Python environment
python --version
pip list | grep torch

# Check file permissions
ls -la scripts/
ls -la src/

# Test individual components
python -c "from src.models.layout_detector import LayoutDetector; print('Layout detector imported successfully')"

# Check dataset integrity
python -c "import cv2; img = cv2.imread('data/enhanced_processed_complete/images/doc_00000_processed.png'); print(f'Image loaded: {img.shape if img is not None else \"Failed\"}')"
```

## **📝 NOTES FOR FUTURE EXECUTION**

1. **Environment**: Always activate the virtual environment first
2. **GPU**: Ensure CUDA is available and RTX 2070 is detected
3. **Dependencies**: All required packages are installed in the virtual environment
4. **Data**: Ensure `data/train/` contains your training dataset
5. **Output**: Results will be saved in `outputs/` and `results/` directories
6. **Model**: Trained model will be saved as `best.pt` in the training output directory

This documentation provides everything you need to reproduce the complete Stage 1 pipeline in the future! 🎉