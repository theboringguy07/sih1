from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from services.recommendation_engine import RecommendationEngine
from services.resume_parser import ResumeParser
from services.translation_service import TranslationService
from data.sample_data import get_sample_internships

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize services
recommendation_engine = RecommendationEngine()
resume_parser = ResumeParser()
translation_service = TranslationService()

# Sample internships data
internships = get_sample_internships()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/internships', methods=['GET'])
def get_internships():
    """Get all available internships"""
    return jsonify(internships)

@app.route('/api/recommend', methods=['POST'])
def recommend_internships():
    """Get personalized internship recommendations with multilingual support"""
    try:
        user_data = request.get_json() or {}
        
        # Extract target language preference
        target_language = user_data.get('target_language', 'en')

        # Accept partial profiles; default missing fields
        normalized_user = {
            'education': (user_data.get('education') or '').strip(),
            'skills': user_data.get('skills') or [],
            'location': (user_data.get('location') or '').strip(),
            'interests': user_data.get('interests') or []
        }
        # Ensure types
        if not isinstance(normalized_user['skills'], list):
            normalized_user['skills'] = [str(normalized_user['skills'])]
        if not isinstance(normalized_user['interests'], list):
            normalized_user['interests'] = [str(normalized_user['interests'])]

        # Get recommendations
        recommendations = recommendation_engine.get_recommendations(normalized_user, internships)
        
        # Translate recommendations if target language is not English
        if target_language != 'en':
            recommendations = translation_service.translate_recommendations(
                recommendations, target_language
            )

        return jsonify({
            "recommendations": recommendations,
            "count": len(recommendations),
            "target_language": target_language,
            "translation_applied": target_language != 'en'
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    """Parse uploaded resume to extract profile data"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Parse resume
        parsed_data = resume_parser.parse(file)
        
        return jsonify(parsed_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """Translate text to regional languages"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        target_language = data.get('target_language', 'hi')  
        
        translated_text = translation_service.translate(text, target_language)
        
        return jsonify({
            "original_text": text,
            "translated_text": translated_text,
            "target_language": target_language
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/profile', methods=['POST'])
def create_profile():
    """Create or update user profile"""
    try:
        profile_data = request.get_json()
        
        # Validate profile data
        if not profile_data:
            return jsonify({"error": "No profile data provided"}), 400
        
        # In a real application, you would save this to a database
        return jsonify({
            "message": "Profile created successfully",
            "profile": profile_data
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    try:
        languages = translation_service.get_supported_languages()
        return jsonify(languages)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/translation-mode', methods=['GET'])
def get_translation_mode():
    """Get current translation mode and capabilities"""
    try:
        mode_info = translation_service.get_translation_mode()
        return jsonify(mode_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/detect-language', methods=['POST'])
def detect_language():
    """Detect the language of input text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        detected_language = translation_service.detect_language(text)
        normalized_text = translation_service.normalize_text(text, detected_language)
        
        return jsonify({
            "detected_language": detected_language,
            "original_text": text,
            "normalized_text": normalized_text
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process-query', methods=['POST'])
def process_multilingual_query():
    """Process a multilingual user query"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        processed_query = translation_service.process_multilingual_query(query)
        
        return jsonify(processed_query)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
