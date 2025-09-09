import PyPDF2
import docx
import re
from io import BytesIO
from .indic_text_processor import IndicTextProcessor
from .translation_service import TranslationService

# Optional dependencies for better functionality
try:
    from pdf2image import convert_from_bytes
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("WARNING: OCR dependencies not available. Install pillow and pytesseract for better PDF parsing.")

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("WARNING: spaCy not available. Name extraction will use fallback method.")


class ResumeParser:
    def __init__(self):
        # Initialize multilingual text processing
        self.text_processor = IndicTextProcessor()
        self.translation_service = TranslationService()
        
        # Load spaCy model if available
        self.nlp = None
        if SPACY_AVAILABLE: 
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("WARNING: spaCy model 'en_core_web_sm' not found.")
                print("    For better name extraction, install with: python -m spacy download en_core_web_sm")
                self.nlp = None

        # Multilingual skills dictionary (extendable)
        self.skills_keywords = {
            'en': [
                'python', 'java', 'javascript', 'html', 'css', 'react', 'angular', 'vue',
                'node.js', 'express', 'django', 'flask', 'spring', 'sql', 'mysql', 'postgresql',
                'mongodb', 'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'linux',
                'windows', 'photoshop', 'illustrator', 'figma', 'sketch', 'autocad', 'solidworks',
                'excel', 'powerpoint', 'word', 'tableau', 'power bi', 'r', 'matlab', 'tensorflow',
                'pytorch', 'machine learning', 'deep learning', 'data science', 'analytics',
                'marketing', 'seo', 'content writing', 'social media', 'communication',
                'leadership', 'project management', 'agile', 'scrum', 'teamwork', 'problem solving'
            ],
            'hi': [
                'पायथन', 'जावा', 'प्रोग्रामिंग', 'कंप्यूटर', 'सॉफ्टवेयर', 'डेटा',
                'मशीन लर्निंग', 'कृत्रिम बुद्धिमत्ता', 'वेब डेवलपमेंट', 'मोबाइल',
                'डिजाइन', 'मार्केटिंग', 'बिक्री', 'प्रबंधन', 'नेतृत्व', 'संचार',
                'टीमवर्क', 'समस्या समाधान', 'विश्लेषण', 'रिपोर्टिंग'
            ],
            'te': [
                'ప్రోగ్రామింగ్', 'కంప్యూటర్', 'సాఫ్ట్‌వేర్', 'డేటా', 'వెబ్ డెవలప్‌మెంట్',
                'మొబైల్', 'డిజైన్', 'మార్కెటింగ్', 'సేల్స్', 'మేనేజ్‌మెంట్',
                'లీడర్‌షిప్', 'కమ్యూనికేషన్', 'టీమ్‌వర్క్', 'సమస్య పరిష్కారం'
            ],
            'ta': [
                'நிரலாக்கம்', 'கணினி', 'மென்பொருள்', 'தரவு', 'வலை மேம்பாடு',
                'மொபைல்', 'வடிவமைப்பு', 'சந்தைப்படுத்தல்', 'விற்பனை', 'மேலாண்மை',
                'தலைமைத்துவம்', 'தகவல்தொடர்பு', 'குழு வேலை', 'சிக்கல் தீர்வு'
            ],
            'bn': [
                'প্রোগ্রামিং', 'কম্পিউটার', 'সফটওয়্যার', 'ডাটা', 'ওয়েব ডেভেলপমেন্ট',
                'মোবাইল', 'ডিজাইন', 'মার্কেটিং', 'সেলস', 'ম্যানেজমেন্ট',
                'লিডারশিপ', 'কমিউনিকেশন', 'টিমওয়ার্ক', 'সমস্যা সমাধান'
            ]
        }

        # Education patterns (multilingual)
        self.education_patterns = {
            'en': [
                r'b\.?tech|bachelor.*technology|engineering',
                r'b\.?sc|bachelor.*science',
                r'b\.?com|bachelor.*commerce',
                r'b\.?a|bachelor.*arts',
                r'm\.?tech|master.*technology',
                r'm\.?sc|master.*science',
                r'mba|master.*business',
                r'diploma|polytechnic',
                r'12th|class.*12|higher.*secondary|intermediate',
                r'10th|class.*10|matriculation|secondary'
            ],
            'hi': [
                r'बी\.?टेक|इंजीनियरिंग|तकनीकी',
                r'बी\.?एससी|विज्ञान',
                r'बी\.?कॉम|वाणिज्य',
                r'बी\.?ए|कला',
                r'एम\.?टेक|प्रौद्योगिकी',
                r'एम\.?एससी|विज्ञान',
                r'एमबीए|बिजनेस|व्यापार',
                r'डिप्लोमा|पॉलिटेक्निक',
                r'12वीं|कक्षा.*12|उच्च माध्यमिक|इंटरमीडिएट',
                r'10वीं|कक्षा.*10|मैट्रिक|माध्यमिक'
            ],
            'te': [
                r'బీ\.?టెక్|ఇంజనీరింగ్|టెక్నాలజీ',
                r'బీ\.?ఎస్సీ|సైన్స్',
                r'బీ\.?కామ్|కామర్స్',
                r'బీ\.?ఏ|ఆర్ట్స్',
                r'ఎం\.?టెక్|టెక్నాలజీ',
                r'ఎం\.?ఎస్సీ|సైన్స్',
                r'ఎంబీఏ|బిజినెస్',
                r'డిప్లొమా|పాలిటెక్నిక్',
                r'12వ|తరగతి.*12|ఇంటర్మీడియట్',
                r'10వ|తరగతి.*10|మెట్రిక్|సెకండరీ'
            ],
            'ta': [
                r'பி\.?டெக்|இன்ஜினியரிங்|தொழில்நுட்பம்',
                r'பி\.?எஸ்சி|அறிவியல்',
                r'பி\.?காம்|வணிகம்',
                r'பி\.?ஏ|கலை',
                r'எம்\.?டெக்|தொழில்நுட்பம்',
                r'எம்\.?எஸ்சி|அறிவியல்',
                r'எம்பிஏ|பிசினஸ்',
                r'டிப்ளமோ|பாலிடெக்னிக்',
                r'12ஆம்|வகுப்பு.*12|உயர்நிலை',
                r'10ஆம்|வகுப்பு.*10|மெட்ரிக்|செகண்டரி'
            ],
            'bn': [
                r'বি\.?টেক|ইঞ্জিনিয়ারিং|প্রযুক্তি',
                r'বি\.?এসসি|বিজ্ঞান',
                r'বি\.?কম|বাণিজ্য',
                r'বি\.?এ|কলা',
                r'এম\.?টেক|প্রযুক্তি',
                r'এম\.?এসসি|বিজ্ঞান',
                r'এমবিএ|ব্যবসা',
                r'ডিপ্লোমা|পলিটেকনিক',
                r'12তম|শ্রেণী.*12|উচ্চ মাধ্যমিক',
                r'10ম|শ্রেণী.*10|মাধ্যমিক'
            ]
        }

        # Indian cities/states
        self.indian_locations = [
            'mumbai', 'delhi', 'bangalore', 'kolkata', 'chennai', 'hyderabad',
            'pune', 'ahmedabad', 'surat', 'jaipur', 'lucknow', 'kanpur',
            'nagpur', 'indore', 'thane', 'bhopal', 'visakhapatnam', 'patna',
            'vadodara', 'ghaziabad', 'ludhiana', 'agra', 'nashik', 'faridabad',
            'meerut', 'rajkot', 'kalyan', 'vasai', 'virar', 'varanasi',
            'andhra pradesh', 'maharashtra', 'tamil nadu', 'karnataka',
            'gujarat', 'rajasthan', 'west bengal', 'madhya pradesh',
            'telangana', 'kerala', 'punjab', 'haryana', 'bihar', 'odisha',
            'uttar pradesh', 'assam', 'jharkhand', 'himachal pradesh',
            'uttarakhand', 'chhattisgarh', 'goa', 'tripura', 'manipur',
            'meghalaya', 'nagaland', 'mizoram', 'arunachal pradesh', 'sikkim'
        ]
    
    def parse(self, file):
        """Main function to parse resume file with multilingual support"""
        try:
            filename = file.filename.lower()
            print(f"📄 Parsing file: {filename}")

            # Extract text from file
            if filename.endswith('.pdf'):
                text = self._extract_text_from_pdf(file)
            elif filename.endswith('.docx') or filename.endswith('.doc'):
                text = self._extract_text_from_docx(file)
            else:
                file.seek(0)
                text = file.read().decode('utf-8')

            print("\n🔍 Extracted text preview:\n", text[:500], "\n---")

            # Process with multilingual capabilities
            parsed_data = self._parse_text_multilingual(text)
            return {
                "success": True, 
                "data": parsed_data, 
                "message": "Resume parsed successfully"
            }

        except Exception as e:
            return {
                "success": False, 
                "data": {}, 
                "message": f"Error parsing resume: {str(e)}"
            }
    
    def _parse_text_multilingual(self, text):
        """Parse extracted text with multilingual support"""
        
        # Detect the primary language of the text
        detected_language = self.text_processor.detect_language(text)
        print(f"🌐 Detected language: {detected_language}")
        
        # Clean and normalize the text
        cleaned_text = self.text_processor.clean_text(text, detected_language)
        normalized_text = self.text_processor.normalize_text(cleaned_text, detected_language)
        
        # Parse different sections
        parsed_data = {
            "detected_language": detected_language,
            "name": self._extract_name_multilingual(normalized_text, detected_language),
            "email": self._extract_email(normalized_text),
            "phone": self._extract_phone(normalized_text),
            "education": self._extract_education_multilingual(normalized_text, detected_language),
            "location": self._extract_location_multilingual(normalized_text, detected_language),
            "skills": self._extract_skills_multilingual(normalized_text, detected_language)
        }
        
        # If the resume is not in English, also provide English translations
        if detected_language != 'en':
            parsed_data["translations"] = {
                "education_en": self.translation_service.translate(
                    parsed_data["education"], 'en'
                ) if parsed_data["education"] != "Not specified" else "Not specified",
                "location_en": self.translation_service.translate(
                    parsed_data["location"], 'en'
                ) if parsed_data["location"] != "Not specified" else "Not specified"
            }
        
        return parsed_data
    
    def _extract_skills_multilingual(self, text, language):
        """Extract skills with multilingual support"""
        found_skills = []
        text_lower = text.lower()
        
        # Check skills in detected language
        if language in self.skills_keywords:
            for skill in self.skills_keywords[language]:
                if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
                    found_skills.append(skill.title())
        
        # Also check English skills (common in all resumes)
        for skill in self.skills_keywords['en']:
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
                found_skills.append(skill.title())
        
        # Remove duplicates while preserving order
        unique_skills = list(dict.fromkeys(found_skills))
        return unique_skills[:15]  # Limit to top 15 skills
    
    def _extract_education_multilingual(self, text, language):
        """Extract education with multilingual pattern matching"""
        educations = []
        text_lower = text.lower()
        
        # Check patterns in detected language
        if language in self.education_patterns:
            for pattern in self.education_patterns[language]:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].strip()
                    education_info = ' '.join(context.split())
                    if education_info and education_info not in educations:
                        educations.append(education_info[:150])
        
        # Also check English patterns (common in Indian resumes)
        for pattern in self.education_patterns['en']:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                education_info = ' '.join(context.split())
                if education_info and education_info not in educations:
                    educations.append(education_info[:150])
        
        return educations[0] if educations else "Not specified"
    
    def _extract_location_multilingual(self, text, language):
        """Extract location with multilingual support"""
        text_lower = text.lower()
        
        # First check for known Indian locations (in English)
        for location in self.indian_locations:
            if location in text_lower:
                return location.title()
        
        # Location patterns in different languages
        location_patterns = {
            'en': [
                r'address[:\s]*([^\n]+)',
                r'location[:\s]*([^\n]+)',
                r'city[:\s]*([^\n]+)',
                r'state[:\s]*([^\n]+)',
                r'residence[:\s]*([^\n]+)'
            ],
            'hi': [
                r'पता[:\s]*([^\n]+)',
                r'स्थान[:\s]*([^\n]+)',
                r'शहर[:\s]*([^\n]+)',
                r'राज्य[:\s]*([^\n]+)',
                r'निवास[:\s]*([^\n]+)'
            ],
            'te': [
                r'చిరునామా[:\s]*([^\n]+)',
                r'స్థానం[:\s]*([^\n]+)',
                r'పట్టణం[:\s]*([^\n]+)',
                r'రాష్ట్రం[:\s]*([^\n]+)'
            ],
            'ta': [
                r'முகவரி[:\s]*([^\n]+)',
                r'இடம்[:\s]*([^\n]+)',
                r'நகரம்[:\s]*([^\n]+)',
                r'மாநிலம்[:\s]*([^\n]+)'
            ],
            'bn': [
                r'ঠিকানা[:\s]*([^\n]+)',
                r'স্থান[:\s]*([^\n]+)',
                r'শহর[:\s]*([^\n]+)',
                r'রাজ্য[:\s]*([^\n]+)'
            ]
        }
        
        # Check patterns in the detected language first
        if language in location_patterns:
            for pattern in location_patterns[language]:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()[:60]
        
        # Fallback to English patterns
        for pattern in location_patterns['en']:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                return match.group(1).strip()[:60]
        
        return "Not specified"
    
    def _extract_name_multilingual(self, text, language):
        """Extract name with multilingual support"""
        
        # First try spaCy if available (works best for English)
        if self.nlp and language == 'en':
            doc = self.nlp(text[:500])
            for entity in doc.ents:
                if entity.label_ == "PERSON":
                    return entity.text
        
        # Multilingual name patterns
        name_patterns = {
            'en': [r'^([A-Z][a-z]+ [A-Z][a-z]+)', r'name[:\s]*([A-Z][a-z]+ [A-Z][a-z]+)'],
            'hi': [r'^नाम[:\s]*([^न\n]+)', r'^([अ-ह]+ [अ-ह]+)'],
            'te': [r'^పేరు[:\s]*([^న\n]+)', r'^([అ-హ]+ [అ-హ]+)'],
            'ta': [r'^பெயர்[:\s]*([^ந\n]+)', r'^([அ-ஹ]+ [அ-ஹ]+)'],
            'bn': [r'^নাম[:\s]*([^ন\n]+)', r'^([অ-হ]+ [অ-হ]+)']
        }
        
        # Try language-specific patterns first
        if language in name_patterns:
            for pattern in name_patterns[language]:
                for line in text.split("\n")[:8]:
                    match = re.search(pattern, line.strip(), re.IGNORECASE)
                    if match:
                        return match.group(1).strip()
        
        # Fallback: look for the first meaningful line
        for line in text.split("\n")[:5]:
            line = line.strip()
            if (3 < len(line) < 50 and 
                not any(char.isdigit() for char in line) and 
                '@' not in line and 
                ':' not in line):
                return line
        
        return "Not found"


    def _extract_text_from_pdf(self, file):
        """Extract text from PDF with OCR fallback"""
        try:
            file.seek(0)
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

            # OCR fallback if no text (only if OCR is available)
            if not text.strip() and OCR_AVAILABLE:
                print("WARNING: No text found, using OCR fallback...")
                file.seek(0)
                images = convert_from_bytes(file.read())
                for img in images:
                    text += pytesseract.image_to_string(img) + "\n"
            elif not text.strip():
                print("WARNING: No text found in PDF and OCR not available.")

            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

    def _extract_text_from_docx(self, file):
        """Extract text from DOCX"""
        try:
            file.seek(0)
            doc = docx.Document(file)
            text = "\n".join([p.text for p in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    def _extract_email(self, text):
        """Extract email address (language-independent)"""
        matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        return matches[0] if matches else "Not found"

    def _extract_phone(self, text):
        """Extract phone number (language-independent)"""
        patterns = [
            r'\+91[-\s]?\d{10}',
            r'\d{10}',
            r'\d{3}[-\s]?\d{3}[-\s]?\d{4}'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return "Not found"
