# PS-05 Stage 1: Document Layout Detection

## Overview

This repository contains the complete implementation for **Stage 1** of the PS-05 Intelligent Multilingual Document Understanding challenge. Stage 1 focuses exclusively on **document layout detection** - identifying and localizing different elements within document images.

## Stage 1 Requirements

### Input
- JPEG/PNG document images (may be rotated, blurred, or noisy)
- Images can contain various document types: contracts, academic papers, business reports, forms, etc.

### Output
- JSON format with bounding box coordinates `[x, y, w, h]` for each detected element
- 6 layout classes:
  - `0: "Background"`
  - `1: "Text"`
  - `2: "Title"`
  - `3: "List"`
  - `4: "Table"`
  - `5: "Figure"`

### Evaluation Metric
- **mAP (Mean Average Precision)** at bbox threshold >= 0.5
- 100% weight for classification and localization

### Timeline
- **Mock Dataset**: Available from 15 Sep 2025
- **Shortlisting Dataset**: Released 4 Nov 2025
- **Solution Submission**: Due by 5 Nov 2025

## Implementation Status

✅ **COMPLETED** - Stage 1 is fully implemented and ready for training

### What's Implemented
1. **Layout Detection Model**: YOLOv8-based detector for 6 layout classes
2. **Dataset Preparation**: Scripts to convert annotations to YOLO format
3. **Training Pipeline**: Complete training workflow with validation
4. **Evaluation**: mAP calculation at IoU threshold >= 0.5
5. **Inference Pipeline**: Ready-to-use layout detection
6. **Testing**: Comprehensive test suite

## Quick Start

### 1. Test the Implementation
```bash
# Run Stage 1 tests
python test_stage1.py
```

### 2. Prepare Training Data
```bash
# Convert existing annotations to YOLO format
python scripts/prepare_dataset.py --data data/train --output data/yolo_dataset
```

### 3. Train the Model
```bash
# Complete Stage 1 training pipeline
python scripts/train_stage1.py --data data/train --output outputs/stage1 --epochs 100
```

### 4. Run Inference
```bash
# Process a single image
python ps05.py infer --input test_image.png --output results/ --stage 1

# Process multiple images
python ps05.py infer --input data/images/ --output results/ --batch --stage 1
```

### 5. Evaluate Performance
```bash
# Evaluate Stage 1 performance
python src/evaluation/stage1_evaluator.py --predictions predictions.json --ground-truth ground_truth.json
```

## Architecture

### Core Components

#### 1. Layout Detector (`src/models/layout_detector.py`)
- **Backbone**: YOLOv8x
- **Classes**: 6 layout classes (Background, Text, Title, List, Table, Figure)
- **Input**: Document images (640x640)
- **Output**: Bounding boxes with class predictions and confidence scores

#### 2. Dataset Preparation (`scripts/prepare_dataset.py`)
- Converts JSON annotations to YOLO format
- Creates train/val/test splits
- Generates dataset.yaml for training

#### 3. Training Pipeline (`scripts/train_stage1.py`)
- Complete training workflow
- Model validation
- Submission package creation

#### 4. Stage 1 Evaluator (`src/evaluation/stage1_evaluator.py`)
- Calculates mAP at IoU threshold >= 0.5
- Per-class precision/recall metrics
- COCO format evaluation support

#### 5. Main Pipeline (`src/pipeline/infer_page.py`)
- End-to-end document processing
- Stage 1: Layout detection only
- Stage 2: + OCR + Language ID (future)
- Stage 3: + Natural Language generation (future)

## Training Data

### Current Dataset
- **Location**: `data/train/`
- **Format**: PNG images + JSON annotations
- **Classes**: Text (category_id: 1), Title (category_id: 2)
- **Size**: ~50+ annotated documents

### Dataset Structure
```
data/train/
├── doc_04998.png
├── doc_04998.json
├── doc_04997.png
├── doc_04997.json
└── ...
```

### Annotation Format
```json
{
  "file_name": "doc_04998.png",
  "annotations": [
    {
      "bbox": [56.82, 393.41, 240.5, 126.58],
      "category_id": 1,
      "category_name": ""
    }
  ]
}
```

## Model Training

### Training Configuration
- **Framework**: YOLOv8
- **Input Size**: 640x640
- **Batch Size**: 8 (configurable)
- **Learning Rate**: 0.001 (configurable)
- **Epochs**: 100 (configurable)

### Training Commands
```bash
# Basic training
python scripts/train_stage1.py --data data/train --output outputs/stage1

# Custom parameters
python scripts/train_stage1.py \
  --data data/train \
  --output outputs/stage1 \
  --epochs 200 \
  --batch-size 16 \
  --learning-rate 0.0005

# Skip dataset preparation (if already done)
python scripts/train_stage1.py \
  --data data/train \
  --output outputs/stage1 \
  --skip-dataset-prep

# Create submission package
python scripts/train_stage1.py \
  --data data/train \
  --output outputs/stage1 \
  --create-submission
```

## Output Format

### Stage 1 JSON Output
```json
{
  "page": 1,
  "size": {"w": 800, "h": 600},
  "elements": [
    {
      "bbox": [50, 100, 200, 50],
      "cls": "Title",
      "score": 0.95,
      "class_id": 2
    },
    {
      "bbox": [50, 200, 500, 100],
      "cls": "Text",
      "score": 0.88,
      "class_id": 1
    }
  ],
  "preprocess": {"deskew_angle": 0.0},
  "processing_time": 0.15
}
```

## Performance Evaluation

### Metrics
- **mAP**: Mean Average Precision at IoU ≥ 0.5
- **Per-class AP**: Average Precision for each layout class
- **Precision/Recall**: Overall precision and recall

### Evaluation Commands
```bash
# Evaluate predictions
python src/evaluation/stage1_evaluator.py \
  --predictions predictions.json \
  --ground-truth ground_truth.json \
  --output evaluation_results.json
```

## Testing

### Run All Tests
```bash
python test_stage1.py
```

### Individual Tests
```bash
# Test layout detector
python -c "from src.models.layout_detector import LayoutDetector; print('Layout detector works!')"

# Test dataset preparation
python scripts/prepare_dataset.py --data data/train --output test_output

# Test pipeline
python ps05.py infer --input test_document.png --output test_results/ --stage 1
```

## File Structure

```
├── src/
│   ├── models/
│   │   └── layout_detector.py      # Layout detection model
│   ├── pipeline/
│   │   └── infer_page.py          # Main processing pipeline
│   └── evaluation/
│       └── stage1_evaluator.py    # Stage 1 evaluation
├── scripts/
│   ├── prepare_dataset.py          # Dataset preparation
│   └── train_stage1.py            # Training pipeline
├── configs/
│   └── ps05_config.yaml           # Configuration
├── data/
│   └── train/                     # Training data
├── models/                         # Trained models
├── test_stage1.py                 # Stage 1 tests
└── STAGE1_README.md               # This file
```

## Configuration

### Key Settings (`configs/ps05_config.yaml`)
```yaml
models:
  layout:
    type: "yolo"
    backbone: "yolov8x"
    classes: ["Background", "Text", "Title", "List", "Table", "Figure"]
    confidence_threshold: 0.5
    nms_threshold: 0.45
    input_size: [640, 640]

training:
  batch_size: 8
  learning_rate: 0.001
  epochs: 100
```

## Dependencies

### Required Packages
```bash
pip install -r requirements.txt
```

### Key Dependencies
- `torch>=2.0.0` - PyTorch
- `ultralytics>=8.0.0` - YOLOv8
- `opencv-python>=4.8.0` - Image processing
- `pyyaml>=6.0` - Configuration
- `pycocotools>=2.0.6` - Evaluation metrics

## Next Steps

### Immediate Actions
1. **Test the implementation**: Run `python test_stage1.py`
2. **Prepare dataset**: Convert annotations to YOLO format
3. **Train model**: Run the training pipeline
4. **Validate**: Test on sample images
5. **Evaluate**: Calculate mAP performance

### For Submission (5 Nov 2025)
1. **Train on full dataset**: Use all available training data
2. **Optimize hyperparameters**: Tune for best mAP performance
3. **Test on mock dataset**: Available from 15 Sep 2025
4. **Prepare submission**: Create final model package
5. **Submit results**: On shortlisting dataset (4 Nov 2025)

## Troubleshooting

### Common Issues

#### 1. Model Loading Failed
```bash
# Check if YOLOv8 is installed
pip install ultralytics

# Verify model file exists
ls -la models/layout_detector.pt
```

#### 2. Dataset Preparation Failed
```bash
# Check data directory structure
ls -la data/train/

# Verify image and annotation files match
python scripts/prepare_dataset.py --data data/train --output test_output
```

#### 3. Training Failed
```bash
# Check GPU availability
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Reduce batch size if memory issues
python scripts/train_stage1.py --batch-size 4
```

### Getting Help
- Check logs for detailed error messages
- Verify all dependencies are installed
- Ensure training data is properly formatted
- Test with smaller datasets first

## Performance Expectations

### Target Metrics
- **mAP ≥ 0.7**: Good performance for Stage 1
- **mAP ≥ 0.8**: Excellent performance
- **mAP ≥ 0.9**: Outstanding performance

### Optimization Tips
1. **Data Augmentation**: Use rotation, scaling, noise
2. **Hyperparameter Tuning**: Learning rate, batch size, epochs
3. **Model Architecture**: Try different YOLOv8 variants
4. **Ensemble Methods**: Combine multiple models

## Conclusion

Stage 1 of PS-05 is **fully implemented and ready for use**. The implementation provides:

- ✅ Complete layout detection pipeline
- ✅ Training and evaluation tools
- ✅ Proper output format for submission
- ✅ Comprehensive testing suite
- ✅ Documentation and examples

**Next milestone**: Train the model on the full dataset and achieve competitive mAP performance for the 5 Nov 2025 submission deadline.

---

**Note**: This implementation focuses exclusively on Stage 1 (layout detection). Stages 2 and 3 (OCR + NL generation) are implemented but not required for the current evaluation.
