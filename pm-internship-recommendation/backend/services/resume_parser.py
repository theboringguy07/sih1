import PyPDF2
import docx
import re
from io import BytesIO
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
        # Load spaCy model if available
        self.nlp = None
        if SPACY_AVAILABLE: 
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("WARNING: spaCy model 'en_core_web_sm' not found.")
                print("    For better name extraction, install with: python -m spacy download en_core_web_sm")
                self.nlp = None

        # Skills dictionary (extendable)
        self.skills_keywords = [
            'python', 'java', 'javascript', 'html', 'css', 'react', 'angular', 'vue',
            'node.js', 'express', 'django', 'flask', 'spring', 'sql', 'mysql', 'postgresql',
            'mongodb', 'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'linux',
            'windows', 'photoshop', 'illustrator', 'figma', 'sketch', 'autocad', 'solidworks',
            'excel', 'powerpoint', 'word', 'tableau', 'power bi', 'r', 'matlab', 'tensorflow',
            'pytorch', 'machine learning', 'deep learning', 'data science', 'analytics',
            'marketing', 'seo', 'content writing', 'social media', 'communication',
            'leadership', 'project management', 'agile', 'scrum', 'teamwork', 'problem solving'
        ]

        # Education patterns
        self.education_patterns = [
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
        ]

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
        """Main function to parse resume file"""
        try:
            filename = file.filename.lower()
            print(f"📄 Parsing file: {filename}")

            if filename.endswith('.pdf'):
                text = self._extract_text_from_pdf(file)
            elif filename.endswith('.docx') or filename.endswith('.doc'):
                text = self._extract_text_from_docx(file)
            else:
                file.seek(0)
                text = file.read().decode('utf-8')

            print("\n🔍 Extracted text preview:\n", text[:500], "\n---")

            parsed_data = self._parse_text(text)
            return {"success": True, "data": parsed_data, "message": "Resume parsed successfully"}

        except Exception as e:
            return {"success": False, "data": {}, "message": f"Error parsing resume: {str(e)}"}

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

    def _parse_text(self, text):
        """Parse extracted text"""
        text_lower = text.lower()

        return {
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "education": self._extract_education(text_lower),
            "location": self._extract_location(text_lower),
            "skills": self._extract_skills(text_lower)
        }

    def _extract_education(self, text):
        educations = []
        for pattern in self.education_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                education_info = ' '.join(context.split())
                if education_info and education_info not in educations:
                    educations.append(education_info[:100])
        return educations[0] if educations else "Not specified"

    def _extract_location(self, text):
        for location in self.indian_locations:
            if location in text:
                return location.title()
        patterns = [
            r'address[:\s]*([^\n]+)',
            r'location[:\s]*([^\n]+)',
            r'city[:\s]*([^\n]+)',
            r'state[:\s]*([^\n]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()[:50]
        return "Not specified"

    def _extract_skills(self, text):
        found_skills = []
        for skill in self.skills_keywords:
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text):
                found_skills.append(skill.title())
        return list(dict.fromkeys(found_skills))[:10]

    def _extract_email(self, text):
        matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        return matches[0] if matches else "Not found"

    def _extract_phone(self, text):
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

    def _extract_name(self, text):
        if self.nlp:
            doc = self.nlp(text[:500])
            for entity in doc.ents:
                if entity.label_ == "PERSON":
                    return entity.text
        # fallback
        for line in text.split("\n")[:5]:
            line = line.strip()
            if 3 < len(line) < 40 and not any(char.isdigit() for char in line) and '@' not in line:
                return line
        return "Not found"
