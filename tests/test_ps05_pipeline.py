"""
Test suite for PS-05 Document Understanding Pipeline
"""

import pytest
import numpy as np
import cv2
import json
import tempfile
import os
from pathlib import Path

# Import our modules
from src.pipeline.infer_page import PS05Pipeline, infer_page
from src.models.layout_detector import LayoutDetector
from src.models.ocr_engine import OCREngine
from src.models.langid_classifier import LanguageClassifier
from src.models.nl_generator import NLGenerator

class TestPS05Pipeline:
    """Test the PS-05 pipeline components."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config_path = "configs/ps05_config.yaml"
        
        # Create a test image
        self.test_image = np.ones((800, 600, 3), dtype=np.uint8) * 255
        
        # Add some test content to the image
        cv2.putText(self.test_image, "Test Document", (50, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
        cv2.putText(self.test_image, "Sample text content", (50, 200), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
    
    def test_layout_detector_initialization(self):
        """Test layout detector initialization."""
        detector = LayoutDetector(self.config_path)
        assert detector is not None
        assert hasattr(detector, 'classes')
        assert len(detector.classes) == 6  # 6 layout classes
    
    def test_layout_detection(self):
        """Test layout detection on test image."""
        detector = LayoutDetector(self.config_path)
        results = detector.predict(self.test_image)
        
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Check result structure
        for result in results:
            assert 'bbox' in result
            assert 'cls' in result
            assert 'score' in result
            assert len(result['bbox']) == 4  # [x, y, w, h]
            assert result['cls'] in detector.classes
            assert 0 <= result['score'] <= 1
    
    def test_ocr_engine_initialization(self):
        """Test OCR engine initialization."""
        ocr = OCREngine(self.config_path)
        assert ocr is not None
        assert hasattr(ocr, 'languages')
        assert len(ocr.languages) >= 6  # 6 target languages
    
    def test_language_classifier_initialization(self):
        """Test language classifier initialization."""
        classifier = LanguageClassifier(self.config_path)
        assert classifier is not None
        assert hasattr(classifier, 'target_languages')
        assert len(classifier.target_languages) == 6
    
    def test_language_detection(self):
        """Test language detection."""
        classifier = LanguageClassifier(self.config_path)
        
        # Test English text
        result = classifier.classify_text("Hello world")
        assert result['lang'] == 'en'
        assert result['confidence'] > 0
        
        # Test Hindi text
        result = classifier.classify_text("नमस्ते दुनिया")
        assert result['lang'] == 'hi'
        assert result['confidence'] > 0
    
    def test_nl_generator_initialization(self):
        """Test NL generator initialization."""
        generator = NLGenerator(self.config_path)
        assert generator is not None
        assert hasattr(generator, 'target_languages')
    
    def test_nl_generation(self):
        """Test natural language generation."""
        generator = NLGenerator(self.config_path)
        
        # Test table summary
        table_data = {'cells': [{'text': 'Sample data', 'row': 0, 'col': 0}]}
        result = generator.generate_table_summary(table_data, self.test_image)
        assert 'summary' in result
        assert 'confidence' in result
        assert len(result['summary']) > 0
    
    def test_pipeline_initialization(self):
        """Test PS-05 pipeline initialization."""
        pipeline = PS05Pipeline(self.config_path)
        assert pipeline is not None
        assert hasattr(pipeline, 'layout_detector')
        assert hasattr(pipeline, 'ocr_engine')
        assert hasattr(pipeline, 'lang_classifier')
        assert hasattr(pipeline, 'nl_generator')
    
    def test_single_image_inference(self):
        """Test single image inference."""
        # Save test image to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            cv2.imwrite(tmp.name, self.test_image)
            image_path = tmp.name
        
        try:
            # Test stage 1 inference
            result = infer_page(image_path, self.config_path, stage=1)
            
            assert isinstance(result, dict)
            assert 'page' in result
            assert 'size' in result
            assert 'elements' in result
            assert 'preprocess' in result
            assert 'processing_time' in result
            
            # Check size
            assert result['size']['w'] == 600
            assert result['size']['h'] == 800
            
            # Check elements
            assert isinstance(result['elements'], list)
            assert len(result['elements']) > 0
            
            # Check preprocessing
            assert 'deskew_angle' in result['preprocess']
            
        finally:
            # Clean up
            if os.path.exists(image_path):
                os.remove(image_path)
    
    def test_pipeline_stages(self):
        """Test different pipeline stages."""
        # Save test image to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            cv2.imwrite(tmp.name, self.test_image)
            image_path = tmp.name
        
        try:
            pipeline = PS05Pipeline(self.config_path)
            
            # Test stage 1
            result1 = pipeline.process_image(image_path, stage=1)
            assert 'elements' in result1
            assert 'text_lines' not in result1
            
            # Test stage 2
            result2 = pipeline.process_image(image_path, stage=2)
            assert 'elements' in result2
            assert 'text_lines' in result2
            
            # Test stage 3
            result3 = pipeline.process_image(image_path, stage=3)
            assert 'elements' in result3
            assert 'text_lines' in result3
            assert 'tables' in result3
            assert 'figures' in result3
            assert 'charts' in result3
            assert 'maps' in result3
            
        finally:
            # Clean up
            if os.path.exists(image_path):
                os.remove(image_path)
    
    def test_output_format(self):
        """Test output format compliance."""
        # Save test image to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            cv2.imwrite(tmp.name, self.test_image)
            image_path = tmp.name
        
        try:
            result = infer_page(image_path, self.config_path, stage=3)
            
            # Test JSON serialization
            json_str = json.dumps(result, ensure_ascii=False)
            parsed_result = json.loads(json_str)
            
            assert parsed_result == result
            
            # Test required fields for stage 1
            required_fields = ['page', 'size', 'elements', 'preprocess']
            for field in required_fields:
                assert field in result
            
            # Test element structure
            for element in result['elements']:
                assert 'id' in element
                assert 'cls' in element
                assert 'bbox' in element
                assert 'score' in element
                assert len(element['bbox']) == 4
            
        finally:
            # Clean up
            if os.path.exists(image_path):
                os.remove(image_path)

def test_config_loading():
    """Test configuration loading."""
    config_path = "configs/ps05_config.yaml"
    
    # Test that config file exists
    assert Path(config_path).exists()
    
    # Test that config can be loaded
    import yaml
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    assert 'system' in config
    assert 'models' in config
    assert 'preprocessing' in config
    assert 'training' in config

def test_error_handling():
    """Test error handling in pipeline."""
    pipeline = PS05Pipeline()
    
    # Test with non-existent image
    result = pipeline.process_image("non_existent_image.png", stage=1)
    assert 'error' in result
    
    # Test with invalid stage
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        cv2.imwrite(tmp.name, np.ones((100, 100, 3), dtype=np.uint8) * 255)
        image_path = tmp.name
    
    try:
        # This should work even with invalid stage (should default to stage 1)
        result = pipeline.process_image(image_path, stage=99)
        assert 'elements' in result
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 