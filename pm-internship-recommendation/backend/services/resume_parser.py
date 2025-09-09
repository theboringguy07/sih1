import PyPDF2
import docx
import re
import spacy
from io import BytesIO

class ResumeParser:
    def __init__(self):
        # Load spaCy model (you might need to download it first)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model 'en_core_web_sm' not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Predefined skills list (can be extended)
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
        
        # Indian cities and states for location detection
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
        """
        Parse resume file and extract relevant information
        """
        try:
            # Extract text based on file type
            filename = file.filename.lower()
            
            if filename.endswith('.pdf'):
                text = self._extract_text_from_pdf(file)
            elif filename.endswith('.docx') or filename.endswith('.doc'):
                text = self._extract_text_from_docx(file)
            else:
                # Try to read as plain text
                text = file.read().decode('utf-8')
            
            # Parse extracted text
            parsed_data = self._parse_text(text)
            
            return {
                'success': True,
                'data': parsed_data,
                'message': 'Resume parsed successfully'
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': {},
                'message': f'Error parsing resume: {str(e)}'
            }

    def _extract_text_from_pdf(self, file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

    def _extract_text_from_docx(self, file):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(BytesIO(file.read()))
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")

    def _parse_text(self, text):
        """Parse extracted text to find education, location, and skills"""
        text_lower = text.lower()
        
        # Extract education
        education = self._extract_education(text_lower)
        
        # Extract location
        location = self._extract_location(text_lower)
        
        # Extract skills
        skills = self._extract_skills(text_lower)
        
        # Extract contact information
        email = self._extract_email(text)
        phone = self._extract_phone(text)
        
        # Extract name (basic implementation)
        name = self._extract_name(text)
        
        return {
            'name': name,
            'email': email,
            'phone': phone,
            'education': education,
            'location': location,
            'skills': skills
        }

    def _extract_education(self, text):
        """Extract education information"""
        educations = []
        
        for pattern in self.education_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get some context around the match
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                
                # Clean up the context
                education_info = ' '.join(context.split())
                if education_info and education_info not in educations:
                    educations.append(education_info[:100])  # Limit length
        
        return educations[0] if educations else "Not specified"

    def _extract_location(self, text):
        """Extract location information"""
        for location in self.indian_locations:
            if location in text:
                return location.title()
        
        # Try to find address patterns
        address_patterns = [
            r'address[:\s]*([^\n]+)',
            r'location[:\s]*([^\n]+)',
            r'city[:\s]*([^\n]+)',
            r'state[:\s]*([^\n]+)'
        ]
        
        for pattern in address_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()[:50]  # Limit length
                return location
        
        return "Not specified"

    def _extract_skills(self, text):
        """Extract skills from text"""
        found_skills = []
        
        for skill in self.skills_keywords:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text):
                found_skills.append(skill.title())
        
        # Remove duplicates while preserving order
        unique_skills = []
        for skill in found_skills:
            if skill not in unique_skills:
                unique_skills.append(skill)
        
        return unique_skills[:10]  # Return top 10 skills

    def _extract_email(self, text):
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else "Not found"

    def _extract_phone(self, text):
        """Extract phone number (Indian format)"""
        phone_patterns = [
            r'\+91[-\s]?\d{10}',
            r'\d{10}',
            r'\d{3}[-\s]?\d{3}[-\s]?\d{4}'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        
        return "Not found"

    def _extract_name(self, text):
        """Extract name (basic implementation using spaCy if available)"""
        if self.nlp:
            doc = self.nlp(text[:500])  # Process first 500 characters
            
            # Look for person names
            for entity in doc.ents:
                if entity.label_ == "PERSON":
                    return entity.text
        
        # Fallback: try to find name patterns
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if len(line.split()) <= 3 and len(line) > 3 and not '@' in line:
                # Simple heuristic: short line without email
                if not any(char.isdigit() for char in line):
                    return line
        
        return "Not found"
