"""
Indic NLP Text Processing Utilities

This module provides comprehensive text processing capabilities using the 
Indic NLP Library for Indian languages. It includes normalization, 
tokenization, script detection, and other language processing features.
"""

import os
import re

# Indic NLP Library imports
try:
    from indicnlp import common
    from indicnlp.tokenize import indic_tokenize, sentence_tokenize
    from indicnlp.normalize import indic_normalize
    from indicnlp.script import indic_scripts
    from indicnlp.transliterate import unicode_transliterate
    from indicnlp.morph import unsupervised_morph
    _INDIC_NLP_AVAILABLE = True
except ImportError:
    _INDIC_NLP_AVAILABLE = False


class IndicTextProcessor:
    """
    Comprehensive text processor using Indic NLP Library features
    """
    
    def __init__(self):
        self.available = _INDIC_NLP_AVAILABLE
        
        # Language code mappings
        self.supported_languages = {
            'hi': 'hindi',
            'te': 'telugu', 
            'ta': 'tamil',
            'bn': 'bengali',
            'gu': 'gujarati',
            'pa': 'punjabi',
            'mr': 'marathi',
            'kn': 'kannada',
            'ml': 'malayalam',
            'or': 'oriya',
            'as': 'assamese'
        }
        
        # Script to language mapping
        self.script_to_lang = {
            'DEVANAGARI': 'hi',
            'TELUGU': 'te',
            'TAMIL': 'ta',
            'BENGALI': 'bn',
            'GUJARATI': 'gu',
            'GURMUKHI': 'pa',
            'KANNADA': 'kn',
            'MALAYALAM': 'ml',
            'ORIYA': 'or',
            'LATIN': 'en'
        }
        
        # Unicode ranges for different scripts
        self.unicode_ranges = {
            'hi': (0x0900, 0x097F),  # Devanagari
            'te': (0x0C00, 0x0C7F),  # Telugu
            'ta': (0x0B80, 0x0BFF),  # Tamil
            'bn': (0x0980, 0x09FF),  # Bengali
            'gu': (0x0A80, 0x0AFF),  # Gujarati
            'pa': (0x0A00, 0x0A7F),  # Gurmukhi
            'mr': (0x0900, 0x097F),  # Marathi (uses Devanagari)
            'kn': (0x0C80, 0x0CFF),  # Kannada
            'ml': (0x0D00, 0x0D7F),  # Malayalam
            'or': (0x0B00, 0x0B7F),  # Oriya
        }
        
        # Initialize Indic NLP if available
        if self.available:
            self._initialize_indic_nlp()
    
    def _initialize_indic_nlp(self):
        """Initialize Indic NLP Library with data path"""
        try:
            # Try to set up data path
            indic_data_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 'data', 'indic_nlp_data'
            )
            if os.path.exists(indic_data_path):
                common.set_resources_path(indic_data_path)
        except Exception as e:
            print(f"Indic NLP initialization warning: {e}")
    
    def detect_script(self, text):
        """
        Detect the script of the input text
        """
        if not self.available:
            return self._fallback_script_detection(text)
        
        try:
            detected_script = indic_scripts.get_script(text)
            return detected_script
        except Exception:
            return self._fallback_script_detection(text)
    
    def _fallback_script_detection(self, text):
        """Fallback script detection using Unicode ranges"""
        char_counts = {}
        
        for char in text:
            for lang, (start, end) in self.unicode_ranges.items():
                if start <= ord(char) <= end:
                    char_counts[lang] = char_counts.get(lang, 0) + 1
        
        if char_counts:
            detected_lang = max(char_counts, key=char_counts.get)
            # Convert language code to script name
            for script, lang in self.script_to_lang.items():
                if lang == detected_lang:
                    return script
        
        return 'LATIN'  # Default to Latin if no Indian script detected
    
    def detect_language(self, text):
        """
        Detect the language of the input text
        """
        script = self.detect_script(text)
        return self.script_to_lang.get(script, 'en')
    
    def normalize_text(self, text, language):
        """
        Normalize text using Indic NLP normalization
        """
        if not self.available or language not in self.supported_languages:
            return text.strip()
        
        try:
            normalized = indic_normalize.normalize(text, language)
            return normalized.strip()
        except Exception:
            return text.strip()
    
    def tokenize_words(self, text, language):
        """
        Tokenize text into words using Indic NLP tokenizer
        """
        if not self.available or language not in self.supported_languages:
            return text.split()
        
        try:
            tokens = indic_tokenize.trivial_tokenize(text, language)
            return list(tokens)
        except Exception:
            return text.split()
    
    def tokenize_sentences(self, text, language):
        """
        Tokenize text into sentences
        """
        if not self.available or language not in self.supported_languages:
            # Simple sentence tokenization fallback
            sentences = re.split(r'[।.!?]+', text)
            return [s.strip() for s in sentences if s.strip()]
        
        try:
            sentences = sentence_tokenize.sentence_split(text, language)
            return sentences
        except Exception:
            # Fallback to regex-based sentence splitting
            sentences = re.split(r'[।.!?]+', text)
            return [s.strip() for s in sentences if s.strip()]
    
    def transliterate(self, text, source_lang, target_lang):
        """
        Transliterate text between Indian languages
        """
        if not self.available or source_lang == target_lang:
            return text
        
        if source_lang not in self.supported_languages or target_lang not in self.supported_languages:
            return text
        
        try:
            transliterated = unicode_transliterate.UnicodeIndicTransliterator.transliterate(
                text, source_lang, target_lang
            )
            return transliterated
        except Exception:
            return text
    
    def morphological_analysis(self, text, language):
        """
        Perform basic morphological analysis
        """
        if not self.available or language not in self.supported_languages:
            return {'words': text.split(), 'stems': text.split()}
        
        try:
            # Tokenize first
            words = self.tokenize_words(text, language)
            
            # Simple stem extraction (if available in Indic NLP)
            stems = []
            for word in words:
                try:
                    # This is a simplified approach - actual morphological analysis
                    # would require more sophisticated models
                    stems.append(word)  # Placeholder
                except Exception:
                    stems.append(word)
            
            return {
                'words': words,
                'stems': stems,
                'language': language,
                'analysis_available': True
            }
        except Exception:
            return {
                'words': text.split(),
                'stems': text.split(),
                'language': language,
                'analysis_available': False
            }
    
    def clean_text(self, text, language=None):
        """
        Clean and preprocess text for better processing
        """
        if not text:
            return text
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep Indian language characters
        if language and language in self.supported_languages:
            # Preserve characters in the language's unicode range
            lang_range = self.unicode_ranges.get(language)
            if lang_range:
                start, end = lang_range
                # Keep alphanumeric, spaces, and language-specific characters
                cleaned = re.sub(
                    rf'[^\w\s{chr(start)}-{chr(end)}।.!?,:;()-]+', 
                    '', 
                    cleaned, 
                    flags=re.UNICODE
                )
        else:
            # General cleaning for unknown language
            cleaned = re.sub(r'[^\w\s।.!?,:;()-]+', '', cleaned, flags=re.UNICODE)
        
        return cleaned.strip()
    
    def extract_keywords(self, text, language):
        """
        Extract keywords from text (simple frequency-based approach)
        """
        words = self.tokenize_words(text, language)
        cleaned_words = self.clean_text(' '.join(words), language).split()
        
        # Remove common stop words (simplified approach)
        stop_words = {
            'hi': {'है', 'हैं', 'का', 'की', 'के', 'में', 'से', 'को', 'और', 'या'},
            'te': {'ఉంది', 'ఉన్నది', 'కు', 'లో', 'మరియు', 'లేదా'},
            'ta': {'உள்ளது', 'உள்ளன', 'இல்', 'கு', 'மற்றும்', 'அல்லது'},
            'bn': {'আছে', 'এর', 'তে', 'এবং', 'অথবা'},
            'en': {'is', 'are', 'the', 'and', 'or', 'in', 'at', 'of', 'to', 'for'}
        }
        
        lang_stop_words = stop_words.get(language, set())
        
        # Filter out stop words and short words
        keywords = [
            word for word in cleaned_words 
            if len(word) > 2 and word.lower() not in lang_stop_words
        ]
        
        # Count frequency
        word_freq = {}
        for word in keywords:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_keywords[:10]]  # Top 10 keywords
    
    def is_supported_language(self, language_code):
        """Check if a language is supported"""
        return language_code in self.supported_languages or language_code == 'en'
    
    def get_language_info(self, language_code):
        """Get information about a supported language"""
        if language_code == 'en':
            return {
                'code': 'en',
                'name': 'English',
                'script': 'LATIN',
                'supported_features': ['basic_processing']
            }
        
        if language_code in self.supported_languages:
            return {
                'code': language_code,
                'name': self.supported_languages[language_code],
                'script': next(
                    (script for script, lang in self.script_to_lang.items() 
                     if lang == language_code), 
                    'UNKNOWN'
                ),
                'supported_features': [
                    'normalization', 
                    'tokenization', 
                    'transliteration', 
                    'script_detection'
                ] if self.available else ['basic_processing']
            }
        
        return None
