@echo off
echo Starting PM Internship Recommendation Frontend...
cd frontend

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing npm dependencies...
    npm install
)

REM Start React development server
echo Starting React development server...
npm start
pause
