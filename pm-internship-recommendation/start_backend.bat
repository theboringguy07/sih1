@echo off
echo Starting PM Internship Recommendation Backend...
cd backend

REM Check if virtual environment exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Download spaCy model if not present
echo Checking spaCy model...
python -c "import spacy; spacy.load('en_core_web_sm')" 2>nul || python -m spacy download en_core_web_sm

REM Start Flask application
echo Starting Flask server...
python app.py
pause
