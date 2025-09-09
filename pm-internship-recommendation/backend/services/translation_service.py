"""
Comprehensive multilingual service using Indic NLP Library.

This service uses the Indic NLP Library for text processing, normalization,
transliteration, and language detection. It includes fallback modes and
rule-based translation for common terms.
"""

# Indic NLP Library imports
try:
    from indicnlp import common
    from indicnlp.tokenize import indic_tokenize
    from indicnlp.normalize import indic_normalize
    from indicnlp.script import indic_scripts
    from indicnlp.transliterate import unicode_transliterate
    import os
    import re
    _INDIC_NLP_AVAILABLE = True
except Exception:
    _INDIC_NLP_AVAILABLE = False

# Optional neural dependencies (heavy). Wrapped to avoid import-time crashes.
try:
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer  # type: ignore
    import torch  # type: ignore
    _NEURAL_DEPS_AVAILABLE = True
except Exception:
    AutoModelForSeq2SeqLM = None  # type: ignore
    AutoTokenizer = None  # type: ignore
    torch = None  # type: ignore
    _NEURAL_DEPS_AVAILABLE = False

class TranslationService:
    def __init__(self):
        # Initialize Indic NLP Library if available
        self.indic_nlp_available = _INDIC_NLP_AVAILABLE
        self.neural_available = _NEURAL_DEPS_AVAILABLE
        
        # Set working mode based on available dependencies
        if self.neural_available:
            self.mode = "neural"
        elif self.indic_nlp_available:
            self.mode = "indic_nlp"
        else:
            self.mode = "fallback"

        # Initialize Indic NLP if available
        if self.indic_nlp_available:
            try:
                # Set up Indic NLP data path (adjust as needed)
                self.indic_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'indic_nlp_data')
                if os.path.exists(self.indic_data_path):
                    common.set_resources_path(self.indic_data_path)
            except Exception as e:
                print(f"IndIC NLP setup warning: {e}")

        # Neural model setup (for advanced translation)
        self.model_name = "ai4bharat/indictrans2-en-indic-1B"
        self.tokenizer = None
        self.model = None
        self.device = "cpu"

        if self.mode == "neural":
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name, trust_remote_code=True)
                self.device = "cuda" if torch and torch.cuda.is_available() else "cpu"  # type: ignore[attr-defined]
                self.model.to(self.device)
            except Exception as load_error:
                print(f"Neural model unavailable ({load_error}). Using Indic NLP mode.")
                self.mode = "indic_nlp" if self.indic_nlp_available else "fallback"
                self.tokenizer = None
                self.model = None

        # Language codes and script mapping
        self.language_map = {
            'en': 'eng_Latn',
            'hi': 'hin_Deva',
            'te': 'tel_Telu',
            'ta': 'tam_Taml',
            'bn': 'ben_Beng'
        }
        
        # Script to language mapping for detection
        self.script_to_lang = {
            'DEVANAGARI': 'hi',
            'TELUGU': 'te',
            'TAMIL': 'ta',
            'BENGALI': 'bn',
            'LATIN': 'en'
        }
        
        # Rule-based translation dictionary for common terms
        self.translation_dict = {
            'en_to_hi': {
                'internship': 'इंटर्नशिप',
                'skills': 'कौशल',
                'education': 'शिक्षा', 
                'experience': 'अनुभव',
                'company': 'कंपनी',
                'job': 'नौकरी',
                'apply': 'आवेदन करें',
                'profile': 'प्रोफ़ाइल',
                'resume': 'रिज्यूमे',
                'qualification': 'योग्यता',
                'requirement': 'आवश्यकता',
                'location': 'स्थान',
                'salary': 'वेतन',
                'duration': 'अवधि',
                'description': 'विवरण'
            },
            'en_to_te': {
                'internship': 'ఇంటర్న్‌షిప్',
                'skills': 'నైపుణ్యాలు',
                'education': 'విద్య',
                'experience': 'అనుభవం',
                'company': 'కంపెనీ',
                'job': 'ఉద్యోగం',
                'apply': 'దరఖాస్తు చేయండి',
                'profile': 'ప్రొఫైల్',
                'resume': 'రెజ్యూమ్',
                'qualification': 'అర్హత',
                'requirement': 'అవసరం',
                'location': 'ప్రాంతం',
                'salary': 'జీతం',
                'duration': 'వ్యవధి',
                'description': 'వివరణ'
            },
            'en_to_ta': {
                'internship': 'பயிற்சி',
                'skills': 'திறமைகள்',
                'education': 'கல்வி',
                'experience': 'அனுபவம்',
                'company': 'நிறுவனம்',
                'job': 'வேலை',
                'apply': 'விண்ணப்பிக்கவும்',
                'profile': 'சுயவிவரம்',
                'resume': 'விவரக்குறிப்பு',
                'qualification': 'தகுதி',
                'requirement': 'தேவை',
                'location': 'இடம்',
                'salary': 'சம்பளம்',
                'duration': 'கால அளவு',
                'description': 'விளக்கம்'
            },
            'en_to_bn': {
                'internship': 'ইন্টার্নশিপ',
                'skills': 'দক্ষতা',
                'education': 'শিক্ষা',
                'experience': 'অভিজ্ঞতা',
                'company': 'কোম্পানি',
                'job': 'চাকরি',
                'apply': 'আবেদন করুন',
                'profile': 'প্রোফাইল',
                'resume': 'জীবনবৃত্তান্ত',
                'qualification': 'যোগ্যতা',
                'requirement': 'প্রয়োজন',
                'location': 'অবস্থান',
                'salary': 'বেতন',
                'duration': 'সময়কাল',
                'description': 'বিবরণ'
            }
        }

    def detect_language(self, text):
        """
        Detect the script/language of the input text using Indic NLP
        """
        if not self.indic_nlp_available:
            return 'en'  # Default fallback
        
        try:
            # Use script detection from Indic NLP
            detected_script = indic_scripts.get_script(text)
            return self.script_to_lang.get(detected_script, 'en')
        except Exception:
            # Fallback: simple heuristic based on character ranges
            if any('\u0900' <= char <= '\u097F' for char in text):
                return 'hi'  # Devanagari
            elif any('\u0C00' <= char <= '\u0C7F' for char in text):
                return 'te'  # Telugu
            elif any('\u0B80' <= char <= '\u0BFF' for char in text):
                return 'ta'  # Tamil
            elif any('\u0980' <= char <= '\u09FF' for char in text):
                return 'bn'  # Bengali
            else:
                return 'en'  # Latin/English
    
    def normalize_text(self, text, language):
        """
        Normalize text using Indic NLP normalization
        """
        if not self.indic_nlp_available or language == 'en':
            return text.strip()
        
        try:
            normalized = indic_normalize.normalize(text, language)
            return normalized.strip()
        except Exception:
            return text.strip()
    
    def tokenize_text(self, text, language):
        """
        Tokenize text using Indic NLP tokenizer
        """
        if not self.indic_nlp_available or language == 'en':
            return text.split()
        
        try:
            tokens = indic_tokenize.trivial_tokenize(text, language)
            return tokens
        except Exception:
            return text.split()
    
    def transliterate_text(self, text, source_lang, target_lang):
        """
        Transliterate text between Indian language scripts
        """
        if not self.indic_nlp_available or source_lang == target_lang:
            return text
        
        try:
            transliterated = unicode_transliterate.UnicodeIndicTransliterator.transliterate(
                text, source_lang, target_lang
            )
            return transliterated
        except Exception:
            return text
    
    def rule_based_translate(self, text, target_language):
        """
        Perform rule-based translation using predefined dictionaries
        """
        if target_language == 'en':
            return text
        
        dict_key = f'en_to_{target_language}'
        if dict_key not in self.translation_dict:
            return text
        
        translation_map = self.translation_dict[dict_key]
        translated_text = text.lower()
        
        # Replace known terms
        for english_term, native_term in translation_map.items():
            translated_text = re.sub(
                r'\b' + re.escape(english_term) + r'\b', 
                native_term, 
                translated_text, 
                flags=re.IGNORECASE
            )
        
        return translated_text

    def translate(self, text, target_language='hi'):
        """
        Comprehensive translation using multiple approaches
        """
        try:
            if target_language not in self.language_map:
                return text
            
            # Step 1: Normalize input text
            source_lang = self.detect_language(text)
            normalized_text = self.normalize_text(text, source_lang)
            
            # If already in target language, return normalized version
            if source_lang == target_language:
                return normalized_text
            
            # Step 2: Try neural translation if available
            if self.mode == "neural" and self.model and self.tokenizer:
                try:
                    tgt_lang = self.language_map[target_language]
                    
                    inputs = self.tokenizer(
                        normalized_text,
                        return_tensors="pt",
                        padding=True,
                        truncation=True
                    ).to(self.device)
                    
                    with torch.no_grad():  # type: ignore[union-attr]
                        generated_tokens = self.model.generate(
                            **inputs,
                            forced_bos_token_id=self.tokenizer.lang_code_to_id[tgt_lang]
                        )
                    
                    translated_text = self.tokenizer.batch_decode(
                        generated_tokens,
                        skip_special_tokens=True
                    )[0]
                    
                    return translated_text
                
                except Exception as neural_error:
                    print(f"Neural translation failed: {neural_error}. Falling back to rule-based.")
            
            # Step 3: Rule-based translation with Indic NLP processing
            if source_lang == 'en':
                # English to Indian language
                rule_translated = self.rule_based_translate(normalized_text, target_language)
                return self.normalize_text(rule_translated, target_language)
            else:
                # Indian language to Indian language via transliteration
                if self.indic_nlp_available and source_lang != 'en' and target_language != 'en':
                    transliterated = self.transliterate_text(normalized_text, source_lang, target_language)
                    return self.normalize_text(transliterated, target_language)
            
            # Fallback: return normalized original text
            return normalized_text
            
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return text

    def get_supported_languages(self):
        """Get list of supported languages with their native names"""
        return {
            'en': 'English',
            'hi': 'हिंदी (Hindi)',
            'te': 'తెలుగు (Telugu)',
            'ta': 'தமிழ் (Tamil)',
            'bn': 'বাংলা (Bengali)'
        }
    
    def get_translation_mode(self):
        """Get current translation mode and capabilities"""
        return {
            'mode': self.mode,
            'indic_nlp_available': self.indic_nlp_available,
            'neural_available': self.neural_available,
            'features': {
                'language_detection': self.indic_nlp_available,
                'text_normalization': self.indic_nlp_available,
                'transliteration': self.indic_nlp_available,
                'neural_translation': self.mode == 'neural',
                'rule_based_translation': True
            }
        }

    def translate_internship_data(self, internship, target_language):
        """Enhanced translation of internship data with better field handling"""
        if target_language == 'en':
            return internship

        translated_internship = internship.copy()
        
        # Fields that should be translated
        text_fields = ['title', 'company', 'description', 'sector', 'location']
        
        for field in text_fields:
            if field in translated_internship and translated_internship[field]:
                original_text = str(translated_internship[field])
                # First detect the language of the original text
                detected_lang = self.detect_language(original_text)
                
                # Only translate if it's different from target language
                if detected_lang != target_language:
                    translated_internship[field] = self.translate(
                        original_text,
                        target_language
                    )
                else:
                    # Normalize the text in the target language
                    translated_internship[field] = self.normalize_text(
                        original_text, target_language
                    )
        
        # Handle nested requirements
        if 'requirements' in translated_internship and translated_internship['requirements']:
            requirements = translated_internship['requirements']
            
            # Translate skills array
            if 'skills' in requirements and requirements['skills']:
                translated_skills = []
                for skill in requirements['skills']:
                    if skill:
                        skill_lang = self.detect_language(str(skill))
                        if skill_lang != target_language:
                            translated_skill = self.translate(str(skill), target_language)
                        else:
                            translated_skill = self.normalize_text(str(skill), target_language)
                        translated_skills.append(translated_skill)
                translated_internship['requirements']['skills'] = translated_skills
            
            # Translate education field if present
            if 'education' in requirements and requirements['education']:
                education_text = str(requirements['education'])
                edu_lang = self.detect_language(education_text)
                if edu_lang != target_language:
                    translated_internship['requirements']['education'] = self.translate(
                        education_text, target_language
                    )
                else:
                    translated_internship['requirements']['education'] = self.normalize_text(
                        education_text, target_language
                    )
        
        # Handle additional fields
        other_translatable_fields = ['benefits', 'responsibilities', 'application_process']
        for field in other_translatable_fields:
            if field in translated_internship and translated_internship[field]:
                field_text = str(translated_internship[field])
                field_lang = self.detect_language(field_text)
                if field_lang != target_language:
                    translated_internship[field] = self.translate(field_text, target_language)
                else:
                    translated_internship[field] = self.normalize_text(field_text, target_language)
        
        return translated_internship

    def translate_recommendations(self, recommendations, target_language):
        """Enhanced translation of recommendation results with comprehensive field handling"""
        if target_language == 'en':
            return recommendations

        translated_recommendations = []
        for recommendation in recommendations:
            # First translate the basic internship data
            translated_rec = self.translate_internship_data(recommendation, target_language)
            
            # Handle match reasons with language detection and normalization
            if 'match_reasons' in translated_rec and translated_rec['match_reasons']:
                translated_reasons = []
                for reason in translated_rec['match_reasons']:
                    if reason:
                        reason_text = str(reason)
                        reason_lang = self.detect_language(reason_text)
                        if reason_lang != target_language:
                            translated_reason = self.translate(reason_text, target_language)
                        else:
                            translated_reason = self.normalize_text(reason_text, target_language)
                        translated_reasons.append(translated_reason)
                translated_rec['match_reasons'] = translated_reasons
            
            # Handle additional recommendation-specific fields
            recommendation_fields = ['match_explanation', 'why_recommended', 'next_steps']
            for field in recommendation_fields:
                if field in translated_rec and translated_rec[field]:
                    field_text = str(translated_rec[field])
                    field_lang = self.detect_language(field_text)
                    if field_lang != target_language:
                        translated_rec[field] = self.translate(field_text, target_language)
                    else:
                        translated_rec[field] = self.normalize_text(field_text, target_language)
            
            translated_recommendations.append(translated_rec)

        return translated_recommendations
    
    def process_multilingual_query(self, query_text):
        """Process a user query that might be in multiple languages"""
        
        # Detect the language of the query
        detected_lang = self.detect_language(query_text)
        
        # Normalize the text in the detected language
        normalized_query = self.normalize_text(query_text, detected_lang)
        
        # Tokenize for better processing
        tokens = self.tokenize_text(normalized_query, detected_lang)
        
        return {
            'original_text': query_text,
            'detected_language': detected_lang,
            'normalized_text': normalized_query,
            'tokens': tokens,
            'translation_to_english': self.translate(normalized_query, 'en') if detected_lang != 'en' else normalized_query
        }
