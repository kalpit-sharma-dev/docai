"""
Test Script for Stage 2 and 3: Multilingual Document Understanding
Tests OCR, Language Detection, and Natural Language Generation capabilities
"""

import cv2
import numpy as np
import json
import logging
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_document():
    """Create a test document with multiple languages and visual elements"""
    # Create a test image with text and visual elements
    img = np.ones((800, 1200, 3), dtype=np.uint8) * 255
    
    # Add some text regions (simulating different languages)
    cv2.putText(img, "Document Title", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img, "This is English text", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(img, "यह हिंदी टेक्स्ट है", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(img, "هذا نص عربي", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Add a table region
    cv2.rectangle(img, (50, 250), (400, 400), (0, 0, 0), 2)
    cv2.putText(img, "Table Data", (60, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # Add a chart region
    cv2.rectangle(img, (450, 250), (800, 400), (0, 0, 0), 2)
    cv2.putText(img, "Chart Data", (460, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # Add a map region
    cv2.rectangle(img, (850, 250), (1150, 400), (0, 0, 0), 2)
    cv2.putText(img, "Map Data", (860, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # Add more text in different languages
    cv2.putText(img, "More English content", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(img, "अधिक हिंदी सामग्री", (50, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(img, "محتوى عربي إضافي", (50, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # Save test document
    test_path = "test_stage2_document.png"
    cv2.imwrite(test_path, img)
    logger.info(f"Test document created: {test_path}")
    
    return test_path

def test_multilingual_ocr():
    """Test multilingual OCR functionality"""
    logger.info("Testing Multilingual OCR...")
    
    try:
        from ocr.multilingual_ocr import MultilingualOCR
        
        # Initialize OCR
        ocr = MultilingualOCR(use_gpu=False)  # Use CPU for testing
        
        # Create test image
        test_img = np.ones((200, 400, 3), dtype=np.uint8) * 255
        cv2.putText(test_img, "Test Text", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Test text extraction
        result = ocr.extract_text(test_img)
        
        logger.info(f"OCR Result: {len(result.text_regions)} text regions detected")
        logger.info(f"Overall text: {result.overall_text[:100]}...")
        logger.info(f"Detected languages: {result.detected_languages}")
        
        # Test CER/WER calculation
        test_gt = "Test Text"
        metrics = ocr.calculate_cer_wer(result.overall_text, test_gt)
        logger.info(f"CER: {metrics['cer_percentage']:.2f}%, WER: {metrics['wer_percentage']:.2f}%")
        
        logger.info("✅ Multilingual OCR test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Multilingual OCR test failed: {e}")
        return False

def test_language_detection():
    """Test language detection functionality"""
    logger.info("Testing Language Detection...")
    
    try:
        from ocr.language_detector import LanguageDetector
        
        # Initialize language detector
        detector = LanguageDetector()
        
        # Test different languages
        test_texts = [
            "This is English text",
            "यह हिंदी टेक्स्ट है",
            "هذا نص عربي",
            "This is mixed English and हिंदी text"
        ]
        
        results = []
        for text in test_texts:
            result = detector.detect_language(text, method='ensemble')
            results.append(result)
            logger.info(f"Text: {text[:30]}... -> Language: {result.detected_language} (confidence: {result.confidence:.2f})")
        
        # Test batch detection
        batch_results = detector.batch_detect(test_texts)
        logger.info(f"Batch detection: {len(batch_results)} results")
        
        # Test metrics calculation (with dummy ground truth)
        gt_languages = ['en', 'hi', 'ar', 'en']
        pred_languages = [r.language_code for r in results]
        metrics = detector.calculate_metrics(pred_languages, gt_languages)
        
        logger.info(f"Language Detection Metrics - Accuracy: {metrics.accuracy:.2f}, F1: {metrics.f1_score:.2f}")
        
        logger.info("✅ Language Detection test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Language Detection test failed: {e}")
        return False

def test_visual_to_text():
    """Test visual to text generation"""
    logger.info("Testing Visual to Text Generation...")
    
    try:
        from nlg.visual_to_text import VisualToTextGenerator
        
        # Initialize generator
        generator = VisualToTextGenerator(use_gpu=False)  # Use CPU for testing
        
        # Create test images for different element types
        test_images = []
        element_types = []
        
        # Table image
        table_img = np.ones((200, 300, 3), dtype=np.uint8) * 255
        cv2.rectangle(table_img, (20, 20), (280, 180), (0, 0, 0), 2)
        cv2.putText(table_img, "Table", (120, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        test_images.append(table_img)
        element_types.append('table')
        
        # Chart image
        chart_img = np.ones((200, 300, 3), dtype=np.uint8) * 255
        cv2.rectangle(chart_img, (20, 20), (280, 180), (0, 0, 0), 2)
        cv2.putText(chart_img, "Chart", (120, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        test_images.append(chart_img)
        element_types.append('chart')
        
        # Map image
        map_img = np.ones((200, 300, 3), dtype=np.uint8) * 255
        cv2.rectangle(map_img, (20, 20), (280, 180), (0, 0, 0), 2)
        cv2.putText(map_img, "Map", (120, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        test_images.append(map_img)
        element_types.append('map')
        
        # Test generation
        bboxes = [[0, 0, 300, 200]] * 3  # Same bbox for all
        
        for i, (img, elem_type, bbox) in enumerate(zip(test_images, element_types, bboxes)):
            result = generator.generate_description(img, bbox, elem_type)
            logger.info(f"{elem_type.capitalize()} description: {result.generated_text[:100]}...")
        
        # Test batch generation
        batch_results = generator.batch_generate(test_images, bboxes, element_types)
        logger.info(f"Batch generation: {len(batch_results)} results")
        
        # Test evaluation
        test_gt = "This is a test description"
        for result in batch_results:
            metrics = generator.evaluate_generation(result.generated_text, test_gt, result.element_type)
            logger.info(f"{result.element_type} evaluation - Combined score: {metrics.combined_score:.3f}")
        
        logger.info("✅ Visual to Text Generation test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Visual to Text Generation test failed: {e}")
        return False

def test_stage2_pipeline():
    """Test Stage 2 pipeline"""
    logger.info("Testing Stage 2 Pipeline...")
    
    try:
        from pipeline.stage2_pipeline import Stage2Pipeline
        
        # Initialize pipeline
        pipeline = Stage2Pipeline(config={'use_gpu': False})
        
        # Create test document
        test_doc_path = create_test_document()
        
        # Process document
        result = pipeline.process_document(test_doc_path)
        
        logger.info(f"Stage 2 processing completed in {result.processing_time:.2f}s")
        logger.info(f"Layout elements: {len(result.layout_elements)}")
        logger.info(f"Text regions: {len(result.text_regions)}")
        logger.info(f"Visual descriptions: {len(result.visual_descriptions)}")
        logger.info(f"Detected languages: {result.detected_languages}")
        
        # Save results
        output_path = "test_stage2_results.json"
        pipeline.save_results(result, output_path)
        logger.info(f"Results saved to: {output_path}")
        
        # Test evaluation (with dummy ground truth)
        dummy_gt = {
            'layout_gt': [],
            'text_gt': [],
            'language_gt': [],
            'visual_gt': []
        }
        
        eval_results = pipeline.evaluate_performance(result, dummy_gt)
        logger.info(f"Evaluation results: {len(eval_results)} metrics calculated")
        
        logger.info("✅ Stage 2 Pipeline test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Stage 2 Pipeline test failed: {e}")
        return False

def test_stage3_pipeline():
    """Test Stage 3 pipeline"""
    logger.info("Testing Stage 3 Pipeline...")
    
    try:
        from pipeline.stage3_pipeline import Stage3Pipeline
        
        # Initialize pipeline
        pipeline = Stage3Pipeline(config={'use_gpu': False})
        
        # Create test document
        test_doc_path = create_test_document()
        
        # Process document
        result = pipeline.process_document(test_doc_path)
        
        logger.info(f"Stage 3 processing completed in {result.processing_time:.2f}s")
        logger.info(f"Stage 2 result inherited: {result.stage2_result is not None}")
        logger.info(f"Enhanced descriptions: {len(result.enhanced_descriptions)}")
        logger.info(f"Semantic analysis: {result.semantic_analysis.keys()}")
        logger.info(f"Cross references: {len(result.cross_references)}")
        logger.info(f"Summary generation: {result.summary_generation.keys()}")
        
        # Save results
        output_path = "test_stage3_results.json"
        pipeline.save_results(result, output_path)
        logger.info(f"Results saved to: {output_path}")
        
        # Test evaluation
        dummy_gt = {
            'layout_gt': [],
            'text_gt': [],
            'language_gt': [],
            'visual_gt': []
        }
        
        eval_results = pipeline.evaluate_stage3_performance(result, dummy_gt)
        logger.info(f"Stage 3 evaluation results: {len(eval_results)} metrics calculated")
        
        if 'overall_pipeline_score' in eval_results:
            logger.info(f"Overall pipeline score: {eval_results['overall_pipeline_score']:.3f}")
        
        logger.info("✅ Stage 3 Pipeline test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Stage 3 Pipeline test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("Starting Stage 2 and 3 Tests...")
    
    test_results = []
    
    # Test individual components
    test_results.append(("Multilingual OCR", test_multilingual_ocr()))
    test_results.append(("Language Detection", test_language_detection()))
    test_results.append(("Visual to Text Generation", test_visual_to_text()))
    
    # Test pipelines
    test_results.append(("Stage 2 Pipeline", test_stage2_pipeline()))
    test_results.append(("Stage 3 Pipeline", test_stage3_pipeline()))
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("TEST RESULTS SUMMARY")
    logger.info("="*50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All Stage 2 and 3 tests passed successfully!")
        return True
    else:
        logger.error(f"⚠️  {total - passed} tests failed. Please check the logs above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
