from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from services.recommendation_engine import RecommendationEngine
from services.resume_parser import ResumeParser
from services.translation_service import TranslationService
from data.sample_data import get_sample_internships

# Load environment variables safely
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")
    print("Continuing with default configuration...")

app = Flask(__name__)
CORS(app)

# Initialize services
recommendation_engine = RecommendationEngine()
resume_parser = ResumeParser()
translation_service = TranslationService()

# Sample internships data
internships = get_sample_internships()

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "message": "PM Internship Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "internships": "/api/internships",
            "recommend": "/api/recommend",
            "parse-resume": "/api/parse-resume",
            "translate": "/api/translate",
            "profile": "/api/profile"
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/internships', methods=['GET'])
def get_internships():
    """Get all available internships"""
    return jsonify(internships)

@app.route('/api/recommend', methods=['POST'])
def recommend_internships():
    """Get personalized internship recommendations"""
    try:
        user_data = request.get_json() or {}

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

        return jsonify({
            "recommendations": recommendations,
            "count": len(recommendations)
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
