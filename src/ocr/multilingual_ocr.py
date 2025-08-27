"""
Multilingual OCR Module for Stage 2
Supports English, Hindi, Urdu, Arabic, Nepalese, Persian
Provides text extraction with CER/WER metrics
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass
from PIL import Image
import easyocr
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TextRegion:
    """Represents a detected text region with metadata"""
    bbox: List[float]  # [x, y, w, h]
    text: str
    confidence: float
    language: str
    language_confidence: float

@dataclass
class OCRResult:
    """Complete OCR result for a document"""
    text_regions: List[TextRegion]
    overall_text: str
    detected_languages: List[str]
    processing_time: float

class MultilingualOCR:
    """
    Multilingual OCR system supporting 6 languages:
    English, Hindi, Urdu, Arabic, Nepalese, Persian
    """
    
    def __init__(self, use_gpu: bool = True):
        self.use_gpu = use_gpu and torch.cuda.is_available()
        self.device = "cuda" if self.use_gpu else "cpu"
        
        # Initialize EasyOCR for multilingual support
        self.languages = ['en', 'hi', 'ur', 'ar', 'ne', 'fa']  # ISO codes
        self.language_names = {
            'en': 'English',
            'hi': 'Hindi', 
            'ur': 'Urdu',
            'ar': 'Arabic',
            'ne': 'Nepalese',
            'fa': 'Persian'
        }
        
        try:
            self.reader = easyocr.Reader(
                self.languages,
                gpu=self.use_gpu,
                model_storage_directory='./models/ocr_models',
                download_enabled=True
            )
            logger.info(f"EasyOCR initialized with languages: {list(self.language_names.values())}")
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR: {e}")
            self.reader = None
            
        # Initialize TrOCR as backup
        try:
            self.trocr_processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
            self.trocr_model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
            if self.use_gpu:
                self.trocr_model.to(self.device)
            logger.info("TrOCR model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load TrOCR model: {e}")
            self.trocr_processor = None
            self.trocr_model = None
    
    def extract_text(self, image: np.ndarray, bbox: Optional[List[float]] = None) -> OCRResult:
        """
        Extract text from image or specific region
        
        Args:
            image: Input image as numpy array
            bbox: Optional bounding box [x, y, w, h] to extract from specific region
            
        Returns:
            OCRResult with extracted text and metadata
        """
        import time
        start_time = time.time()
        
        if bbox:
            # Extract region from image
            x, y, w, h = [int(coord) for coord in bbox]
            image = image[y:y+h, x:x+w]
        
        # Preprocess image
        processed_image = self._preprocess_image(image)
        
        # Extract text using EasyOCR
        if self.reader:
            try:
                results = self.reader.readtext(processed_image)
                text_regions = self._process_easyocr_results(results)
            except Exception as e:
                logger.warning(f"EasyOCR failed: {e}, falling back to TrOCR")
                text_regions = self._extract_with_trocr(processed_image)
        else:
            text_regions = self._extract_with_trocr(processed_image)
        
        # Post-process results
        text_regions = self._post_process_text_regions(text_regions)
        
        # Combine all text
        overall_text = " ".join([region.text for region in text_regions])
        
        # Detect languages
        detected_languages = list(set([region.language for region in text_regions]))
        
        processing_time = time.time() - start_time
        
        return OCRResult(
            text_regions=text_regions,
            overall_text=overall_text,
            detected_languages=detected_languages,
            processing_time=processing_time
        )
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR performance"""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(binary)
        
        # Enhance contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        return enhanced
    
    def _process_easyocr_results(self, results: List[Tuple]) -> List[TextRegion]:
        """Process EasyOCR results into TextRegion objects"""
        text_regions = []
        
        for (bbox, text, confidence) in results:
            # Convert bbox format from EasyOCR to [x, y, w, h]
            x_coords = [point[0] for point in bbox]
            y_coords = [point[1] for point in bbox]
            
            x = min(x_coords)
            y = min(y_coords)
            w = max(x_coords) - x
            h = max(y_coords) - y
            
            # Detect language (simplified - EasyOCR doesn't provide language detection)
            # We'll use a simple heuristic based on character sets
            detected_lang = self._detect_language_from_text(text)
            
            text_region = TextRegion(
                bbox=[x, y, w, h],
                text=text.strip(),
                confidence=confidence,
                language=detected_lang,
                language_confidence=0.8  # Placeholder
            )
            text_regions.append(text_region)
        
        return text_regions
    
    def _extract_with_trocr(self, image: np.ndarray) -> List[TextRegion]:
        """Extract text using TrOCR as fallback"""
        if not self.trocr_processor or not self.trocr_model:
            return []
        
        try:
            # Convert numpy array to PIL Image
            pil_image = Image.fromarray(image)
            
            # Process image
            pixel_values = self.trocr_processor(pil_image, return_tensors="pt").pixel_values
            if self.use_gpu:
                pixel_values = pixel_values.to(self.device)
            
            # Generate text
            generated_ids = self.trocr_model.generate(pixel_values)
            generated_text = self.trocr_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            # Create a single text region for the entire image
            text_region = TextRegion(
                bbox=[0, 0, image.shape[1], image.shape[0]],
                text=generated_text,
                confidence=0.7,  # Placeholder
                language='en',  # TrOCR is primarily English
                language_confidence=0.6
            )
            
            return [text_region]
            
        except Exception as e:
            logger.error(f"TrOCR extraction failed: {e}")
            return []
    
    def _detect_language_from_text(self, text: str) -> str:
        """Simple language detection based on character sets"""
        # Count characters from different scripts
        arabic_chars = len(re.findall(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text))
        devanagari_chars = len(re.findall(r'[\u0900-\u097F]', text))
        urdu_chars = len(re.findall(r'[\u0600-\u06FF]', text))  # Overlaps with Arabic
        persian_chars = len(re.findall(r'[\u0600-\u06FF\uFB50-\uFDFF]', text))  # Overlaps with Arabic
        
        # Simple heuristics
        if arabic_chars > 0:
            if persian_chars > arabic_chars * 0.8:
                return 'fa'  # Persian
            else:
                return 'ar'  # Arabic
        elif devanagari_chars > 0:
            return 'hi'  # Hindi
        elif urdu_chars > 0:
            return 'ur'  # Urdu
        else:
            return 'en'  # Default to English
    
    def _post_process_text_regions(self, text_regions: List[TextRegion]) -> List[TextRegion]:
        """Post-process extracted text regions"""
        processed_regions = []
        
        for region in text_regions:
            # Clean text
            cleaned_text = self._clean_text(region.text)
            if cleaned_text and len(cleaned_text.strip()) > 0:
                region.text = cleaned_text
                processed_regions.append(region)
        
        # Sort by position (top to bottom, left to right)
        processed_regions.sort(key=lambda x: (x.bbox[1], x.bbox[0]))
        
        return processed_regions
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might be OCR artifacts
        text = re.sub(r'[^\w\s\u0600-\u06FF\u0900-\u097F\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', '', text)
        
        return text.strip()
    
    def calculate_cer_wer(self, predicted_text: str, ground_truth_text: str) -> Dict[str, float]:
        """
        Calculate Character Error Rate (CER) and Word Error Rate (WER)
        
        Args:
            predicted_text: Text extracted by OCR
            ground_truth_text: Reference text
            
        Returns:
            Dictionary with CER and WER scores
        """
        from difflib import SequenceMatcher
        
        # Calculate CER
        cer = 1 - SequenceMatcher(None, predicted_text, ground_truth_text).ratio()
        
        # Calculate WER
        pred_words = predicted_text.split()
        gt_words = ground_truth_text.split()
        
        if len(gt_words) == 0:
            wer = 1.0 if len(pred_words) > 0 else 0.0
        else:
            wer = 1 - SequenceMatcher(None, pred_words, gt_words).ratio()
        
        return {
            'cer': cer,
            'wer': wer,
            'cer_percentage': cer * 100,
            'wer_percentage': wer * 100
        }
    
    def batch_extract(self, images: List[np.ndarray], bboxes: Optional[List[List[float]]] = None) -> List[OCRResult]:
        """Extract text from multiple images"""
        results = []
        
        for i, image in enumerate(images):
            bbox = bboxes[i] if bboxes else None
            try:
                result = self.extract_text(image, bbox)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to extract text from image {i}: {e}")
                # Create empty result
                empty_result = OCRResult(
                    text_regions=[],
                    overall_text="",
                    detected_languages=[],
                    processing_time=0.0
                )
                results.append(empty_result)
        
        return results
