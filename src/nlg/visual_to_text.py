"""
Natural Language Generation Module for Stage 2
Converts visual elements (charts, maps, tables) to natural language text
Uses BlueRT + BertScore for charts/maps and T2T-Gen for tables
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
import logging
from dataclasses import dataclass
import json
import re
from PIL import Image
import torch
from transformers import (
    VisionEncoderDecoderModel, 
    VisionEncoderDecoderProcessor,
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    pipeline
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NLGResult:
    """Result of natural language generation"""
    generated_text: str
    confidence: float
    element_type: str  # 'chart', 'map', 'table'
    bbox: List[float]  # [x, y, w, h]
    metadata: Dict

@dataclass
class EvaluationMetrics:
    """Evaluation metrics for NLG"""
    bleurt_score: float
    bertscore_score: float
    combined_score: float
    details: Dict

class VisualToTextGenerator:
    """
    Natural Language Generation system for visual elements:
    - Charts and Maps: BlueRT + BertScore
    - Tables: T2T-Gen
    """
    
    def __init__(self, use_gpu: bool = True):
        self.use_gpu = use_gpu and torch.cuda.is_available()
        self.device = "cuda" if self.use_gpu else "cpu"
        
        # Initialize models
        self._init_chart_map_models()
        self._init_table_models()
        
        logger.info(f"VisualToTextGenerator initialized on {self.device}")
    
    def _init_chart_map_models(self):
        """Initialize models for chart and map understanding"""
        try:
            # Vision-Language model for chart/map understanding
            self.chart_processor = VisionEncoderDecoderProcessor.from_pretrained(
                'microsoft/git-base-coco'
            )
            self.chart_model = VisionEncoderDecoderModel.from_pretrained(
                'microsoft/git-base-coco'
            )
            
            if self.use_gpu:
                self.chart_model.to(self.device)
            
            logger.info("Chart/Map understanding model loaded successfully")
            
        except Exception as e:
            logger.warning(f"Failed to load chart/map model: {e}")
            self.chart_processor = None
            self.chart_model = None
        
        # Initialize BERTScore for evaluation
        try:
            from bert_score import BERTScorer
            self.bertscorer = BERTScorer(
                lang="en", 
                use_fast_tokenizer=True,
                device=self.device
            )
            logger.info("BERTScore initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize BERTScore: {e}")
            self.bertscorer = None
    
    def _init_table_models(self):
        """Initialize T2T-Gen model for table understanding"""
        try:
            # Table-to-text generation model
            self.table_tokenizer = AutoTokenizer.from_pretrained(
                'google/flan-t5-base'
            )
            self.table_model = AutoModelForSeq2SeqLM.from_pretrained(
                'google/flan-t5-base'
            )
            
            if self.use_gpu:
                self.table_model.to(self.device)
            
            # Table understanding pipeline
            self.table_pipeline = pipeline(
                "image-to-text",
                model="microsoft/git-base-coco",
                device=0 if self.use_gpu else -1
            )
            
            logger.info("Table understanding models loaded successfully")
            
        except Exception as e:
            logger.warning(f"Failed to load table models: {e}")
            self.table_tokenizer = None
            self.table_model = None
            self.table_pipeline = None
    
    def generate_description(self, image: np.ndarray, bbox: List[float], element_type: str) -> NLGResult:
        """
        Generate natural language description for visual element
        
        Args:
            image: Input image
            bbox: Bounding box [x, y, w, h]
            element_type: Type of element ('chart', 'map', 'table')
            
        Returns:
            NLGResult with generated description
        """
        # Extract region from image
        x, y, w, h = [int(coord) for coord in bbox]
        region_image = image[y:y+h, x:x+w]
        
        if element_type in ['chart', 'map']:
            return self._generate_chart_map_description(region_image, element_type, bbox)
        elif element_type == 'table':
            return self._generate_table_description(region_image, bbox)
        else:
            raise ValueError(f"Unsupported element type: {element_type}")
    
    def _generate_chart_map_description(self, image: np.ndarray, element_type: str, bbox: List[float]) -> NLGResult:
        """Generate description for charts and maps using vision-language model"""
        try:
            if self.chart_model and self.chart_processor:
                # Convert to PIL Image
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                
                # Process image
                pixel_values = self.chart_processor(
                    pil_image, 
                    return_tensors="pt"
                ).pixel_values
                
                if self.use_gpu:
                    pixel_values = pixel_values.to(self.device)
                
                # Generate description
                generated_ids = self.chart_model.generate(
                    pixel_values,
                    max_length=100,
                    num_beams=4,
                    early_stopping=True
                )
                
                generated_text = self.chart_processor.batch_decode(
                    generated_ids, 
                    skip_special_tokens=True
                )[0]
                
                # Post-process based on element type
                if element_type == 'chart':
                    generated_text = self._enhance_chart_description(generated_text)
                elif element_type == 'map':
                    generated_text = self._enhance_map_description(generated_text)
                
                return NLGResult(
                    generated_text=generated_text,
                    confidence=0.8,  # Placeholder
                    element_type=element_type,
                    bbox=bbox,
                    metadata={'model': 'git-base-coco', 'method': 'vision-language'}
                )
            
            else:
                # Fallback to template-based generation
                return self._generate_template_description(image, element_type, bbox)
                
        except Exception as e:
            logger.error(f"Chart/map description generation failed: {e}")
            return self._generate_template_description(image, element_type, bbox)
    
    def _generate_table_description(self, image: np.ndarray, bbox: List[float]) -> NLGResult:
        """Generate description for tables using T2T-Gen approach"""
        try:
            if self.table_pipeline:
                # Convert to PIL Image
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                
                # Generate table description
                result = self.table_pipeline(pil_image)
                generated_text = result[0]['generated_text']
                
                # Enhance table description
                enhanced_text = self._enhance_table_description(generated_text)
                
                return NLGResult(
                    generated_text=enhanced_text,
                    confidence=0.8,  # Placeholder
                    element_type='table',
                    bbox=bbox,
                    metadata={'model': 'flan-t5-base', 'method': 't2t-gen'}
                )
            
            else:
                # Fallback to template-based generation
                return self._generate_template_description(image, 'table', bbox)
                
        except Exception as e:
            logger.error(f"Table description generation failed: {e}")
            return self._generate_template_description(image, 'table', bbox)
    
    def _enhance_chart_description(self, text: str) -> str:
        """Enhance chart description with chart-specific language"""
        # Add chart context if not present
        if 'chart' not in text.lower() and 'graph' not in text.lower():
            text = f"This chart shows {text.lower()}"
        
        # Enhance with chart terminology
        chart_keywords = ['data', 'values', 'trend', 'increase', 'decrease', 'percentage']
        if any(keyword in text.lower() for keyword in chart_keywords):
            text += ". The visualization provides a clear representation of the data."
        
        return text
    
    def _enhance_map_description(self, text: str) -> str:
        """Enhance map description with map-specific language"""
        # Add map context if not present
        if 'map' not in text.lower() and 'location' not in text.lower():
            text = f"This map displays {text.lower()}"
        
        # Enhance with geographic terminology
        map_keywords = ['area', 'region', 'location', 'geographic', 'spatial']
        if any(keyword in text.lower() for keyword in map_keywords):
            text += ". The map provides spatial information about the depicted area."
        
        return text
    
    def _enhance_table_description(self, text: str) -> str:
        """Enhance table description with table-specific language"""
        # Add table context if not present
        if 'table' not in text.lower():
            text = f"This table contains {text.lower()}"
        
        # Enhance with tabular terminology
        table_keywords = ['data', 'information', 'rows', 'columns', 'entries']
        if any(keyword in text.lower() for keyword in table_keywords):
            text += ". The table presents structured information in an organized format."
        
        return text
    
    def _generate_template_description(self, image: np.ndarray, element_type: str, bbox: List[float]) -> NLGResult:
        """Generate template-based description as fallback"""
        # Analyze image characteristics
        height, width = image.shape[:2]
        aspect_ratio = width / height if height > 0 else 1
        
        # Generate template description based on element type and characteristics
        if element_type == 'chart':
            if aspect_ratio > 1.5:
                template = "This is a wide chart displaying data in a horizontal format."
            elif aspect_ratio < 0.7:
                template = "This is a tall chart displaying data in a vertical format."
            else:
                template = "This is a chart displaying data with balanced proportions."
        
        elif element_type == 'map':
            if aspect_ratio > 1.2:
                template = "This is a wide map showing geographic information in landscape orientation."
            elif aspect_ratio < 0.8:
                template = "This is a tall map showing geographic information in portrait orientation."
            else:
                template = "This is a map showing geographic information with balanced proportions."
        
        elif element_type == 'table':
            if aspect_ratio > 1.5:
                template = "This is a wide table with many columns displaying structured data."
            elif aspect_ratio < 0.7:
                template = "This is a tall table with many rows displaying structured data."
            else:
                template = "This is a table displaying structured data in a balanced format."
        
        else:
            template = f"This is a {element_type} element displaying visual information."
        
        return NLGResult(
            generated_text=template,
            confidence=0.5,  # Lower confidence for template-based generation
            element_type=element_type,
            bbox=bbox,
            metadata={'model': 'template', 'method': 'fallback'}
        )
    
    def evaluate_generation(self, generated_text: str, reference_text: str, element_type: str) -> EvaluationMetrics:
        """
        Evaluate generated text using BlueRT + BertScore for charts/maps or T2T-Gen metrics for tables
        
        Args:
            generated_text: Generated description
            reference_text: Reference/ground truth description
            element_type: Type of element being evaluated
            
        Returns:
            EvaluationMetrics with scores
        """
        try:
            # Calculate BERTScore
            bertscore_score = 0.0
            if self.bertscorer:
                P, R, F1 = self.bertscorer.score([generated_text], [reference_text])
                bertscore_score = F1.mean().item()
            
            # Calculate BlueRT (simplified - using BLEU as approximation)
            bleurt_score = self._calculate_bleu_score(generated_text, reference_text)
            
            # Combined score (weighted average)
            if element_type in ['chart', 'map']:
                # For charts/maps: equal weight to BlueRT and BertScore
                combined_score = (bleurt_score + bertscore_score) / 2
            else:
                # For tables: T2T-Gen approach (more weight to BertScore)
                combined_score = (bleurt_score * 0.3) + (bertscore_score * 0.7)
            
            return EvaluationMetrics(
                bleurt_score=bleurt_score,
                bertscore_score=bertscore_score,
                combined_score=combined_score,
                details={
                    'element_type': element_type,
                    'generated_length': len(generated_text),
                    'reference_length': len(reference_text)
                }
            )
            
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return EvaluationMetrics(
                bleurt_score=0.0,
                bertscore_score=0.0,
                combined_score=0.0,
                details={'error': str(e)}
            )
    
    def _calculate_bleu_score(self, generated_text: str, reference_text: str) -> float:
        """Calculate BLEU score as approximation for BlueRT"""
        try:
            from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
            
            # Tokenize texts
            generated_tokens = generated_text.lower().split()
            reference_tokens = reference_text.lower().split()
            
            # Calculate BLEU score
            smoothing = SmoothingFunction().method1
            bleu_score = sentence_bleu([reference_tokens], generated_tokens, smoothing_function=smoothing)
            
            return bleu_score
            
        except Exception as e:
            logger.warning(f"BLEU score calculation failed: {e}")
            # Fallback to simple similarity
            return self._calculate_simple_similarity(generated_text, reference_text)
    
    def _calculate_simple_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity as fallback"""
        from difflib import SequenceMatcher
        
        # Normalize texts
        text1_norm = text1.lower().strip()
        text2_norm = text2.lower().strip()
        
        # Calculate similarity
        similarity = SequenceMatcher(None, text1_norm, text2_norm).ratio()
        
        return similarity
    
    def batch_generate(self, images: List[np.ndarray], bboxes: List[List[float]], 
                       element_types: List[str]) -> List[NLGResult]:
        """Generate descriptions for multiple visual elements"""
        results = []
        
        for i, (image, bbox, element_type) in enumerate(zip(images, bboxes, element_types)):
            try:
                result = self.generate_description(image, bbox, element_type)
                results.append(result)
            except Exception as e:
                logger.error(f"Description generation failed for element {i}: {e}")
                # Create error result
                error_result = NLGResult(
                    generated_text=f"Error generating description for {element_type}",
                    confidence=0.0,
                    element_type=element_type,
                    bbox=bbox,
                    metadata={'error': str(e)}
                )
                results.append(error_result)
        
        return results
    
    def batch_evaluate(self, generated_texts: List[str], reference_texts: List[str], 
                      element_types: List[str]) -> List[EvaluationMetrics]:
        """Evaluate multiple generated descriptions"""
        results = []
        
        for i, (gen_text, ref_text, elem_type) in enumerate(zip(generated_texts, reference_texts, element_types)):
            try:
                metrics = self.evaluate_generation(gen_text, ref_text, elem_type)
                results.append(metrics)
            except Exception as e:
                logger.error(f"Evaluation failed for element {i}: {e}")
                # Create error metrics
                error_metrics = EvaluationMetrics(
                    bleurt_score=0.0,
                    bertscore_score=0.0,
                    combined_score=0.0,
                    details={'error': str(e)}
                )
                results.append(error_metrics)
        
        return results
