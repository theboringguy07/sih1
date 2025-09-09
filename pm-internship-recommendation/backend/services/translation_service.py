class TranslationService:
    def __init__(self):
        # Basic translation dictionary for common phrases
        # In production, you'd integrate with proper Indic NLP libraries
        self.translations = {
            'hi': {  # Hindi
                'Welcome': 'स्वागत',
                'Internship': 'प्रशिक्षण',
                'Recommendations': 'सिफारिशें',
                'Skills': 'कौशल',
                'Education': 'शिक्षा',
                'Location': 'स्थान',
                'Profile': 'प्रोफ़ाइल',
                'Upload Resume': 'रिज्यूमे अपलोड करें',
                'Get Recommendations': 'सिफारिशें प्राप्त करें',
                'Technology': 'तकनीक',
                'Business': 'व्यापार',
                'Marketing': 'विपणन',
                'Finance': 'वित्त',
                'Engineering': 'इंजीनियरिंग',
                'Submit': 'जमा करें',
                'Next': 'अगला',
                'Back': 'वापस',
                'Search': 'खोजें',
                'Apply Now': 'अभी आवेदन करें',
                'Duration': 'अवधि',
                'Stipend': 'वेतन',
                'Company': 'कंपनी',
                'Description': 'विवरण',
                'Requirements': 'आवश्यकताएं',
                'Name': 'नाम',
                'Email': 'ईमेल',
                'Phone': 'फोन',
                'Age': 'उम्र',
                'Gender': 'लिंग',
                'Address': 'पता',
                'Interests': 'रुचियां',
                'Experience': 'अनुभव',
                'Match Score': 'मैच स्कोर',
                'Why this matches': 'यह क्यों मैच करता है'
            },
            'te': {  # Telugu
                'Welcome': 'స్వాగతం',
                'Internship': 'ఇంటర్న్‌షిప్',
                'Recommendations': 'సిఫార్సులు',
                'Skills': 'నైపుణ్యాలు',
                'Education': 'విద్య',
                'Location': 'స్థానం',
                'Profile': 'ప్రొఫైల్',
                'Upload Resume': 'రెజ్యూమే అప్‌లోడ్ చేయండి',
                'Get Recommendations': 'సిఫార్సులు పొందండి',
                'Technology': 'సాంకేతికత',
                'Business': 'వ్యాపారం',
                'Marketing': 'మార్కెటింగ్',
                'Finance': 'ఫైనాన్స్',
                'Engineering': 'ఇంజనీరింగ్',
                'Submit': 'సమర్పించు',
                'Next': 'తరువాత',
                'Back': 'వెనుకకు',
                'Search': 'వెతకండి',
                'Apply Now': 'ఇప్పుడు దరఖాస్తు చేయండి',
                'Duration': 'వ్యవధి',
                'Stipend': 'స్టైపెండ్',
                'Company': 'కంపెనీ',
                'Description': 'వివరణ',
                'Requirements': 'అవసరాలు'
            },
            'ta': {  # Tamil
                'Welcome': 'வரவேற்கிறோம்',
                'Internship': 'பயிற்சி',
                'Recommendations': 'பரிந்துரைகள்',
                'Skills': 'திறன்கள்',
                'Education': 'கல்வி',
                'Location': 'இடம்',
                'Profile': 'சுயவிவரம்',
                'Upload Resume': 'ரெசுமே பதிவேற்றவும்',
                'Get Recommendations': 'பரிந்துரைகளைப் பெறுங்கள்',
                'Technology': 'தொழில்நுட்பம்',
                'Business': 'வணிகம்',
                'Marketing': 'சந்தைப்படுத்தல்',
                'Finance': 'நிதி',
                'Engineering': 'பொறியியல்',
                'Submit': 'சமர்ப்பிக்கவும்',
                'Next': 'அடுத்தது',
                'Back': 'பின்னால்',
                'Search': 'தேடுங்கள்',
                'Apply Now': 'இப்போது விண்ணప்பிக்கவும்'
            },
            'bn': {  # Bengali
                'Welcome': 'স্বাগতম',
                'Internship': 'ইন্টার্নশিপ',
                'Recommendations': 'সুপারিশ',
                'Skills': 'দক্ষতা',
                'Education': 'শিক্ষা',
                'Location': 'অবস্থান',
                'Profile': 'প্রোফাইল',
                'Upload Resume': 'জীবনবৃত্তান্ত আপলোড করুন',
                'Get Recommendations': 'সুপারিশ পান',
                'Technology': 'প্রযুক্তি',
                'Business': 'ব্যবসা',
                'Marketing': 'বিপণন',
                'Finance': 'অর্থ',
                'Engineering': 'প্রকৌশল',
                'Submit': 'জমা দিন',
                'Next': 'পরবর্তী',
                'Back': 'পেছনে',
                'Search': 'অনুসন্ধান',
                'Apply Now': 'এখনই আবেদন করুন'
            }
        }
    
    def translate(self, text, target_language='hi'):
        """
        Translate text to target language
        This is a basic implementation using dictionary lookup
        In production, integrate with proper Indic NLP translation APIs
        """
        try:
            if target_language not in self.translations:
                return text  # Return original if language not supported
            
            translation_dict = self.translations[target_language]
            
            # Simple word/phrase replacement
            translated_text = text
            for english_text, translated in translation_dict.items():
                translated_text = translated_text.replace(english_text, translated)
            
            return translated_text
        
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return text  # Return original text if translation fails
    
    def get_supported_languages(self):
        """
        Get list of supported languages
        """
        return {
            'en': 'English',
            'hi': 'हिंदी (Hindi)',
            'te': 'తెలుగు (Telugu)',
            'ta': 'தமிழ் (Tamil)',
            'bn': 'বাংলা (Bengali)'
        }
    
    def translate_internship_data(self, internship, target_language):
        """
        Translate internship data to target language
        """
        if target_language == 'en':
            return internship
        
        translated_internship = internship.copy()
        
        # Translate specific fields
        fields_to_translate = ['title', 'company', 'description', 'sector']
        
        for field in fields_to_translate:
            if field in translated_internship:
                translated_internship[field] = self.translate(
                    translated_internship[field], 
                    target_language
                )
        
        # Translate requirements
        if 'requirements' in translated_internship:
            if 'skills' in translated_internship['requirements']:
                translated_skills = []
                for skill in translated_internship['requirements']['skills']:
                    translated_skills.append(self.translate(skill, target_language))
                translated_internship['requirements']['skills'] = translated_skills
        
        return translated_internship
    
    def translate_recommendations(self, recommendations, target_language):
        """
        Translate a list of internship recommendations
        """
        if target_language == 'en':
            return recommendations
        
        translated_recommendations = []
        
        for recommendation in recommendations:
            translated_rec = self.translate_internship_data(recommendation, target_language)
            
            # Translate match reasons
            if 'match_reasons' in translated_rec:
                translated_reasons = []
                for reason in translated_rec['match_reasons']:
                    translated_reasons.append(self.translate(reason, target_language))
                translated_rec['match_reasons'] = translated_reasons
            
            translated_recommendations.append(translated_rec)
        
        return translated_recommendations
