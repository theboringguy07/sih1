# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is an AI-based internship recommendation system for the PM Internship Scheme. The application helps candidates find relevant internship opportunities through resume parsing, skill matching, and multilingual support.

**Tech Stack:**
- **Backend**: Flask (Python) with RESTful APIs
- **Frontend**: React 18 with functional components
- **NLP**: spaCy for resume parsing, Indic NLP Library for translation
- **ML**: Rule-based recommendation engine using fuzzy string matching
- **Development**: Automated setup scripts for rapid deployment

## Architecture

### Backend Architecture (`backend/`)

The Flask backend follows a service-oriented architecture:

- **`app.py`**: Main Flask application with API endpoints
- **`services/`**: Core business logic modules
  - **`recommendation_engine.py`**: Rule-based ML recommendation system with weighted scoring (education 20%, skills 30%, location 30%, interests 20%)
  - **`resume_parser.py`**: Multi-format resume parsing (PDF, DOCX) with spaCy NLP and OCR fallback
  - **`translation_service.py`**: Indic NLP translation service with neural model support (IndicTrans2) and safe fallback mode
- **`data/`**: Sample data and models
  - **`sample_data.py`**: Mock internship data for testing (12 diverse internship samples)

### Frontend Architecture (`frontend/src/`)

React SPA with mobile-first responsive design:

- **`App.js`**: Main application with routing and state management
- **`components/`**: Feature components (Header, ProfileForm, RecommendationsPage, ResumeUpload)
- **`context/`**: Language context for multilingual support
- **`services/`**: API service layer for backend communication

### Key Features

1. **Resume Parsing Pipeline**: PDF/DOCX → Text extraction → NLP analysis → Profile data extraction
2. **Recommendation Engine**: Multi-factor scoring with fuzzy matching for education, skills, location, and interests
3. **Translation Service**: Supports Hindi, Telugu, Tamil, Bengali with neural model fallback
4. **Mobile-Optimized UI**: Touch-friendly interface for low digital literacy users

## Common Development Commands

### One-Command Setup & Run
```bash
# Complete setup and start both servers
python setup.py

# Setup and auto-start (no prompts)
python setup.py --start

# Setup only, don't start servers
python setup.py --no-start

# Skip setup, just run servers
python setup.py --run-only
# or
python run.py
```

### Manual Backend Development
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies and spaCy model
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run development server
python app.py
# Backend available at http://localhost:5000
```

### Manual Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm start
# Frontend available at http://localhost:3000

# Build for production
npm run build

# Run tests
npm test
```

### Quick Start Scripts
```bash
# Windows
start_backend.bat
start_frontend.bat

# Unix-like systems
./start_backend.sh
./start_frontend.sh
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/recommend` | POST | Get personalized recommendations |
| `/api/parse-resume` | POST | Parse uploaded resume files |
| `/api/internships` | GET | Get all available internships |
| `/api/translate` | POST | Translate text to regional languages |
| `/api/profile` | POST | Create/update user profile |

## Development Guidelines

### Backend Services

- **RecommendationEngine**: Uses weighted fuzzy matching with configurable weights. Education patterns are regex-based for robust matching.
- **ResumeParser**: Handles PDF (PyPDF2) and DOCX parsing with OCR fallback. Extracts name (spaCy NER), email/phone (regex), skills (keyword matching), location (Indian cities), and education (pattern matching).
- **TranslationService**: Safe fallback mode to avoid heavy dependencies. Neural mode uses IndicTrans2 when transformers/torch available.

### Frontend Components

- Mobile-first responsive design with touch-friendly UI
- React Router for navigation between profile creation, resume upload, and recommendations
- Language context provider for multilingual support
- Axios for API communication with backend

### Configuration

- **Backend**: Environment variables via `.env` file (Flask debug, CORS origins)
- **Frontend**: Create React App with proxy configuration to backend
- **Dependencies**: Automated dependency management through setup scripts

### Testing & Deployment

- **Backend**: Flask development server for local testing, Gunicorn for production
- **Frontend**: React dev server for development, static build for production deployment
- **Data**: Sample internship data in `sample_data.py` for testing (replace with database in production)

## Recommendation Algorithm

The engine uses a multi-factor weighted scoring system:
1. **Education Match (20%)**: Direct matching + sector alignment using education-to-industry mapping
2. **Skills Match (30%)**: Fuzzy string matching between user and required skills
3. **Location Preference (30%)**: Geographic proximity with remote work support
4. **Interest Alignment (20%)**: Matching user interests with internship sector/description

Score calculation includes match reasons generation for explainable recommendations.

## Multilingual Support

Supports English, Hindi, Telugu, Tamil, and Bengali through:
- UI text translation using language context
- Internship data translation via TranslationService
- Safe fallback to English when neural models unavailable
- Language codes: en, hi, te, ta, bn

## Development Environment Setup

The project includes comprehensive automation:
- **Cross-platform**: Windows (batch) and Unix (shell) start scripts
- **Dependency management**: Automatic Python venv and npm package installation
- **Model download**: Automated spaCy model installation
- **Concurrent servers**: Threaded backend/frontend startup with graceful shutdown
- **Error handling**: Fallback modes for optional dependencies (OCR, neural translation)
