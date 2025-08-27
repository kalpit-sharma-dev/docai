#!/usr/bin/env python3
"""
Stage 1 Test Script for PS-05 Layout Detection

Tests the basic functionality of Stage 1 layout detection.
"""

import cv2
import numpy as np
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_document():
    """Create a test document image for testing."""
    # Create a white background
    img = np.ones((800, 600, 3), dtype=np.uint8) * 255
    
    # Add title
    cv2.putText(img, "Test Document", (50, 100), 
               cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
    
    # Add some text content
    cv2.putText(img, "This is a sample document for testing", (50, 200), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
    cv2.putText(img, "layout detection functionality.", (50, 230), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
    
    # Add a simple table-like structure
    cv2.rectangle(img, (50, 300), (550, 400), (0, 0, 0), 2)
    cv2.putText(img, "Sample Table", (60, 320), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)
    
    # Add a figure placeholder
    cv2.circle(img, (500, 500), 50, (0, 0, 0), 2)
    cv2.putText(img, "Figure", (470, 560), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    return img

def test_layout_detector():
    """Test the layout detector."""
    try:
        from src.models.layout_detector import LayoutDetector
        
        logger.info("Testing Layout Detector...")
        
        # Create test image
        test_img = create_test_document()
        
        # Initialize detector
        detector = LayoutDetector()
        
        # Run prediction
        results = detector.predict(test_img)
        
        logger.info(f"Layout detection completed. Found {len(results)} elements:")
        
        for i, result in enumerate(results):
            bbox = result['bbox']
            cls = result['cls']
            score = result['score']
            logger.info(f"  {i+1}. {cls}: bbox={bbox}, score={score:.3f}")
        
        # Save test image
        test_img_path = "test_document.png"
        cv2.imwrite(test_img_path, test_img)
        logger.info(f"Test image saved to {test_img_path}")
        
        return results
        
    except Exception as e:
        logger.error(f"Layout detector test failed: {e}")
        return None

def test_pipeline_stage1():
    """Test the complete Stage 1 pipeline."""
    try:
        from src.pipeline.infer_page import PS05Pipeline
        
        logger.info("Testing Stage 1 Pipeline...")
        
        # Create test image
        test_img = create_test_document()
        test_img_path = "test_document.png"
        cv2.imwrite(test_img_path, test_img)
        
        # Initialize pipeline
        pipeline = PS05Pipeline()
        
        # Process image with Stage 1 only
        result = pipeline.process_image(test_img_path, stage=1)
        
        logger.info("Stage 1 pipeline test completed successfully!")
        logger.info(f"Processing time: {result.get('processing_time', 0):.2f}s")
        logger.info(f"Found {len(result.get('elements', []))} layout elements")
        
        # Save result
        with open("test_stage1_result.json", 'w') as f:
            json.dump(result, f, indent=2)
        
        logger.info("Test result saved to test_stage1_result.json")
        
        return result
        
    except Exception as e:
        logger.error(f"Stage 1 pipeline test failed: {e}")
        return None

def test_dataset_preparation():
    """Test dataset preparation."""
    try:
        from scripts.prepare_dataset import prepare_dataset
        
        logger.info("Testing Dataset Preparation...")
        
        # Check if training data exists
        data_dir = "data/train"
        if not Path(data_dir).exists():
            logger.warning(f"Training data directory {data_dir} not found")
            return False
        
        # Count files
        image_files = list(Path(data_dir).glob("*.png")) + list(Path(data_dir).glob("*.jpg"))
        json_files = list(Path(data_dir).glob("*.json"))
        
        logger.info(f"Found {len(image_files)} images and {len(json_files)} annotations")
        
        if len(image_files) == 0:
            logger.warning("No training images found")
            return False
        
        # Test dataset preparation
        output_dir = "test_dataset_output"
        dataset_yaml = prepare_dataset(data_dir, output_dir)
        
        if dataset_yaml:
            logger.info(f"Dataset preparation successful: {dataset_yaml}")
            
            # Check output structure
            output_path = Path(output_dir)
            if output_path.exists():
                logger.info("Dataset output structure:")
                for split in ['train', 'val', 'test']:
                    split_path = output_path / split
                    if split_path.exists():
                        img_count = len(list((split_path / "images").glob("*")))
                        label_count = len(list((split_path / "labels").glob("*")))
                        logger.info(f"  {split}: {img_count} images, {label_count} labels")
            
            return True
        else:
            logger.error("Dataset preparation failed")
            return False
            
    except Exception as e:
        logger.error(f"Dataset preparation test failed: {e}")
        return False

def main():
    """Run all Stage 1 tests."""
    logger.info("="*60)
    logger.info("STAGE 1 TESTING")
    logger.info("="*60)
    
    # Test 1: Layout Detector
    logger.info("\n1. Testing Layout Detector...")
    layout_results = test_layout_detector()
    
    # Test 2: Stage 1 Pipeline
    logger.info("\n2. Testing Stage 1 Pipeline...")
    pipeline_results = test_pipeline_stage1()
    
    # Test 3: Dataset Preparation
    logger.info("\n3. Testing Dataset Preparation...")
    dataset_success = test_dataset_preparation()
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("STAGE 1 TEST SUMMARY")
    logger.info("="*60)
    
    if layout_results:
        logger.info("✅ Layout Detector: PASSED")
    else:
        logger.info("❌ Layout Detector: FAILED")
    
    if pipeline_results:
        logger.info("✅ Stage 1 Pipeline: PASSED")
    else:
        logger.info("❌ Stage 1 Pipeline: FAILED")
    
    if dataset_success:
        logger.info("✅ Dataset Preparation: PASSED")
    else:
        logger.info("❌ Dataset Preparation: FAILED")
    
    # Overall status
    if layout_results and pipeline_results and dataset_success:
        logger.info("\n🎉 ALL STAGE 1 TESTS PASSED!")
        logger.info("Stage 1 is ready for training and evaluation.")
    else:
        logger.info("\n⚠️  SOME STAGE 1 TESTS FAILED!")
        logger.info("Please check the errors above and fix them.")
    
    logger.info("="*60)

if __name__ == "__main__":
    main()
