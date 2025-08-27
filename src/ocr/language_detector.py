"""
Language Detection Module for Stage 2
Provides accurate language identification for 6 languages:
English, Hindi, Urdu, Arabic, Nepalese, Persian
"""

import re
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass
from collections import Counter
import langid
from langdetect import detect, detect_langs
from langdetect.lang_detect_exception import LangDetectException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LanguageDetectionResult:
    """Result of language detection for a text region"""
    detected_language: str
    confidence: float
    alternative_languages: List[Tuple[str, float]]
    language_code: str
    is_reliable: bool

@dataclass
class LanguageMetrics:
    """Language detection performance metrics"""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: Dict[str, Dict[str, int]]

class LanguageDetector:
    """
    Advanced language detection system supporting 6 languages:
    English, Hindi, Urdu, Arabic, Nepalese, Persian
    """
    
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'ur': 'Urdu', 
            'ar': 'Arabic',
            'ne': 'Nepalese',
            'fa': 'Persian'
        }
        
        # Character set patterns for each language
        self.language_patterns = {
            'en': r'[a-zA-Z]',
            'hi': r'[\u0900-\u097F]',  # Devanagari
            'ur': r'[\u0600-\u06FF]',  # Arabic (Urdu uses Arabic script)
            'ar': r'[\u0600-\u06FF]',  # Arabic
            'ne': r'[\u0900-\u097F]',  # Nepali uses Devanagari
            'fa': r'[\u0600-\u06FF]'   # Persian uses Arabic script
        }
        
        # Language-specific features
        self.language_features = {
            'en': {
                'common_words': ['the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with'],
                'character_freq': {'e': 0.12, 't': 0.09, 'a': 0.08, 'o': 0.08, 'i': 0.07}
            },
            'hi': {
                'common_words': ['का', 'के', 'की', 'है', 'में', 'और', 'या', 'पर', 'से', 'तक'],
                'character_freq': {'ा': 0.15, 'े': 0.12, 'ी': 0.10, 'क': 0.08, 'म': 0.07}
            },
            'ur': {
                'common_words': ['اور', 'کی', 'کے', 'ہے', 'میں', 'پر', 'سے', 'تک', 'یا', 'لیے'],
                'character_freq': {'ا': 0.12, 'ی': 0.10, 'ر': 0.08, 'ک': 0.07, 'م': 0.06}
            },
            'ar': {
                'common_words': ['في', 'من', 'إلى', 'على', 'عن', 'مع', 'هذا', 'هذه', 'التي', 'الذي'],
                'character_freq': {'ا': 0.15, 'ل': 0.12, 'ي': 0.10, 'ن': 0.08, 'ر': 0.07}
            },
            'ne': {
                'common_words': ['को', 'का', 'की', 'मा', 'र', 'पनि', 'तर', 'अथवा', 'यो', 'त्यो'],
                'character_freq': {'ा': 0.14, 'े': 0.11, 'ी': 0.09, 'क': 0.08, 'म': 0.07}
            },
            'fa': {
                'common_words': ['در', 'از', 'به', 'با', 'که', 'این', 'آن', 'برای', 'تا', 'یا'],
                'character_freq': {'ا': 0.13, 'ی': 0.11, 'ر': 0.09, 'ن': 0.08, 'د': 0.07}
            }
        }
        
        # Initialize language detection libraries
        self._init_langid()
    
    def _init_langid(self):
        """Initialize langid library with custom language mapping"""
        try:
            # Set language detection to focus on our supported languages
            langid.set_languages(list(self.supported_languages.keys()))
            logger.info("LangID initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize LangID: {e}")
    
    def detect_language(self, text: str, method: str = 'ensemble') -> LanguageDetectionResult:
        """
        Detect language using specified method
        
        Args:
            text: Input text to analyze
            method: Detection method ('ensemble', 'langid', 'langdetect', 'pattern', 'feature')
            
        Returns:
            LanguageDetectionResult with detection details
        """
        if not text or len(text.strip()) == 0:
            return LanguageDetectionResult(
                detected_language='Unknown',
                confidence=0.0,
                alternative_languages=[],
                language_code='unknown',
                is_reliable=False
            )
        
        if method == 'ensemble':
            return self._ensemble_detection(text)
        elif method == 'langid':
            return self._detect_with_langid(text)
        elif method == 'langdetect':
            return self._detect_with_langdetect(text)
        elif method == 'pattern':
            return self._detect_with_patterns(text)
        elif method == 'feature':
            return self._detect_with_features(text)
        else:
            raise ValueError(f"Unknown detection method: {method}")
    
    def _ensemble_detection(self, text: str) -> LanguageDetectionResult:
        """Combine multiple detection methods for better accuracy"""
        results = []
        
        # Try different methods
        methods = ['langid', 'langdetect', 'pattern', 'feature']
        for method in methods:
            try:
                result = self.detect_language(text, method)
                if result.is_reliable:
                    results.append(result)
            except Exception as e:
                logger.debug(f"Method {method} failed: {e}")
                continue
        
        if not results:
            # Fallback to pattern-based detection
            return self._detect_with_patterns(text)
        
        # Aggregate results
        language_votes = Counter()
        confidence_sum = {}
        
        for result in results:
            lang_code = result.language_code
            language_votes[lang_code] += 1
            if lang_code not in confidence_sum:
                confidence_sum[lang_code] = 0
            confidence_sum[lang_code] += result.confidence
        
        # Find most voted language
        if language_votes:
            most_voted = language_votes.most_common(1)[0][0]
            confidence = confidence_sum[most_voted] / language_votes[most_voted]
            
            # Get alternative languages
            alternatives = []
            for lang_code, votes in language_votes.most_common():
                if lang_code != most_voted:
                    alt_confidence = confidence_sum[lang_code] / votes
                    alternatives.append((self.supported_languages.get(lang_code, lang_code), alt_confidence))
            
            return LanguageDetectionResult(
                detected_language=self.supported_languages.get(most_voted, most_voted),
                confidence=confidence,
                alternative_languages=alternatives[:3],  # Top 3 alternatives
                language_code=most_voted,
                is_reliable=confidence > 0.6
            )
        
        # Fallback
        return LanguageDetectionResult(
            detected_language='Unknown',
            confidence=0.0,
            alternative_languages=[],
            language_code='unknown',
            is_reliable=False
        )
    
    def _detect_with_langid(self, text: str) -> LanguageDetectionResult:
        """Detect language using langid library"""
        try:
            lang_code, confidence = langid.classify(text)
            
            # Map to our supported languages
            if lang_code in self.supported_languages:
                return LanguageDetectionResult(
                    detected_language=self.supported_languages[lang_code],
                    confidence=confidence,
                    alternative_languages=[],
                    language_code=lang_code,
                    is_reliable=confidence > 0.7
                )
            else:
                # Try to find closest match
                return self._find_closest_language(lang_code, confidence)
                
        except Exception as e:
            logger.debug(f"LangID detection failed: {e}")
            return self._detect_with_patterns(text)
    
    def _detect_with_langdetect(self, text: str) -> LanguageDetectionResult:
        """Detect language using langdetect library"""
        try:
            # Get all possible languages with probabilities
            languages = detect_langs(text)
            
            if languages:
                # Find the best match among our supported languages
                best_match = None
                best_confidence = 0.0
                
                for lang in languages:
                    if lang.lang in self.supported_languages:
                        if lang.prob > best_confidence:
                            best_confidence = lang.prob
                            best_match = lang.lang
                
                if best_match:
                    # Get alternatives
                    alternatives = []
                    for lang in languages:
                        if lang.lang != best_match and lang.lang in self.supported_languages:
                            alternatives.append((self.supported_languages[lang.lang], lang.prob))
                    
                    return LanguageDetectionResult(
                        detected_language=self.supported_languages[best_match],
                        confidence=best_confidence,
                        alternative_languages=alternatives[:3],
                        language_code=best_match,
                        is_reliable=best_confidence > 0.6
                    )
            
            # Fallback to single detection
            try:
                lang_code = detect(text)
                if lang_code in self.supported_languages:
                    return LanguageDetectionResult(
                        detected_language=self.supported_languages[lang_code],
                        confidence=0.8,  # Default confidence
                        alternative_languages=[],
                        language_code=lang_code,
                        is_reliable=True
                    )
            except LangDetectException:
                pass
                
        except Exception as e:
            logger.debug(f"LangDetect detection failed: {e}")
        
        return self._detect_with_patterns(text)
    
    def _detect_with_patterns(self, text: str) -> LanguageDetectionResult:
        """Detect language using character set patterns"""
        scores = {}
        
        for lang_code, pattern in self.language_patterns.items():
            matches = len(re.findall(pattern, text))
            if len(text) > 0:
                scores[lang_code] = matches / len(text)
            else:
                scores[lang_code] = 0.0
        
        if scores:
            best_lang = max(scores, key=scores.get)
            best_score = scores[best_lang]
            
            # Get alternatives
            alternatives = []
            for lang_code, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[1:4]:
                if score > 0.1:  # Only include reasonable alternatives
                    alternatives.append((self.supported_languages[lang_code], score))
            
            return LanguageDetectionResult(
                detected_language=self.supported_languages[best_lang],
                confidence=best_score,
                alternative_languages=alternatives,
                language_code=best_lang,
                is_reliable=best_score > 0.3
            )
        
        return LanguageDetectionResult(
            detected_language='Unknown',
            confidence=0.0,
            alternative_languages=[],
            language_code='unknown',
            is_reliable=False
        )
    
    def _detect_with_features(self, text: str) -> LanguageDetectionResult:
        """Detect language using language-specific features"""
        scores = {}
        
        for lang_code, features in self.language_features.items():
            score = 0.0
            
            # Check common words
            text_lower = text.lower()
            word_matches = sum(1 for word in features['common_words'] if word in text_lower)
            word_score = word_matches / len(features['common_words'])
            
            # Check character frequency
            char_score = 0.0
            if len(text) > 0:
                char_counts = Counter(text.lower())
                total_chars = len(text)
                
                for char, expected_freq in features['character_freq'].items():
                    actual_freq = char_counts.get(char, 0) / total_chars
                    char_score += 1 - abs(expected_freq - actual_freq)
                
                char_score /= len(features['character_freq'])
            
            # Combined score
            score = (word_score * 0.6) + (char_score * 0.4)
            scores[lang_code] = score
        
        if scores:
            best_lang = max(scores, key=scores.get)
            best_score = scores[best_lang]
            
            # Get alternatives
            alternatives = []
            for lang_code, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[1:4]:
                if score > 0.1:
                    alternatives.append((self.supported_languages[lang_code], score))
            
            return LanguageDetectionResult(
                detected_language=self.supported_languages[best_lang],
                confidence=best_score,
                alternative_languages=alternatives,
                language_code=best_lang,
                is_reliable=best_score > 0.4
            )
        
        return LanguageDetectionResult(
            detected_language='Unknown',
            confidence=0.0,
            alternative_languages=[],
            language_code='unknown',
            is_reliable=False
        )
    
    def _find_closest_language(self, detected_lang: str, confidence: float) -> LanguageDetectionResult:
        """Find the closest supported language to the detected one"""
        # Simple mapping for common language codes
        lang_mapping = {
            'en': 'en', 'eng': 'en', 'english': 'en',
            'hi': 'hi', 'hin': 'hi', 'hindi': 'hi',
            'ur': 'ur', 'urd': 'ur', 'urdu': 'ur',
            'ar': 'ar', 'ara': 'ar', 'arabic': 'ar',
            'ne': 'ne', 'nep': 'ne', 'nepali': 'ne',
            'fa': 'fa', 'fas': 'fa', 'persian': 'fa', 'farsi': 'fa'
        }
        
        mapped_lang = lang_mapping.get(detected_lang.lower(), detected_lang.lower())
        
        if mapped_lang in self.supported_languages:
            return LanguageDetectionResult(
                detected_language=self.supported_languages[mapped_lang],
                confidence=confidence * 0.8,  # Reduce confidence due to mapping
                alternative_languages=[],
                language_code=mapped_lang,
                is_reliable=confidence > 0.8
            )
        
        # Default to English if no match
        return LanguageDetectionResult(
            detected_language='English',
            confidence=0.5,
            alternative_languages=[],
            language_code='en',
            is_reliable=False
        )
    
    def batch_detect(self, texts: List[str], method: str = 'ensemble') -> List[LanguageDetectionResult]:
        """Detect languages for multiple texts"""
        results = []
        
        for text in texts:
            try:
                result = self.detect_language(text, method)
                results.append(result)
            except Exception as e:
                logger.error(f"Language detection failed for text: {e}")
                # Create unknown result
                unknown_result = LanguageDetectionResult(
                    detected_language='Unknown',
                    confidence=0.0,
                    alternative_languages=[],
                    language_code='unknown',
                    is_reliable=False
                )
                results.append(unknown_result)
        
        return results
    
    def calculate_metrics(self, predictions: List[str], ground_truth: List[str]) -> LanguageMetrics:
        """
        Calculate language detection performance metrics
        
        Args:
            predictions: Predicted language codes
            ground_truth: Ground truth language codes
            
        Returns:
            LanguageMetrics with accuracy, precision, recall, F1-score
        """
        if len(predictions) != len(ground_truth):
            raise ValueError("Predictions and ground truth must have same length")
        
        # Initialize confusion matrix
        confusion_matrix = {lang: {other_lang: 0 for other_lang in self.supported_languages.keys()} 
                           for lang in self.supported_languages.keys()}
        
        # Fill confusion matrix
        for pred, gt in zip(predictions, ground_truth):
            if pred in self.supported_languages and gt in self.supported_languages:
                confusion_matrix[gt][pred] += 1
        
        # Calculate metrics for each language
        total_correct = 0
        total_predictions = len(predictions)
        
        precision_sum = 0
        recall_sum = 0
        
        for lang_code in self.supported_languages.keys():
            # True positives
            tp = confusion_matrix[lang_code][lang_code]
            
            # False positives (predicted as this language but actually different)
            fp = sum(confusion_matrix[other_lang][lang_code] for other_lang in self.supported_languages.keys() 
                    if other_lang != lang_code)
            
            # False negatives (actually this language but predicted as different)
            fn = sum(confusion_matrix[lang_code][other_lang] for other_lang in self.supported_languages.keys() 
                    if other_lang != lang_code)
            
            total_correct += tp
            
            # Calculate precision and recall for this language
            if tp + fp > 0:
                precision = tp / (tp + fp)
                precision_sum += precision
            
            if tp + fn > 0:
                recall = tp / (tp + fn)
                recall_sum += recall
        
        # Overall metrics
        accuracy = total_correct / total_predictions if total_predictions > 0 else 0
        avg_precision = precision_sum / len(self.supported_languages)
        avg_recall = recall_sum / len(self.supported_languages)
        
        # F1-score
        if avg_precision + avg_recall > 0:
            f1_score = 2 * (avg_precision * avg_recall) / (avg_precision + avg_recall)
        else:
            f1_score = 0
        
        return LanguageMetrics(
            accuracy=accuracy,
            precision=avg_precision,
            recall=avg_recall,
            f1_score=f1_score,
            confusion_matrix=confusion_matrix
        )
