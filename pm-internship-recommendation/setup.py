#!/usr/bin/env python3
"""
Setup script for PM Internship Recommendation Engine
Automates the setup process for both backend and frontend
"""

import os
import sys
import subprocess
import platform

def run_command(command, cwd=None, shell=True):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=shell, 
            check=True, 
            capture_output=True, 
            text=True
        )
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return False

def setup_backend():
    """Setup Flask backend"""
    print("\n🔧 Setting up Backend (Flask)...")
    
    backend_dir = os.path.join(os.getcwd(), 'backend')
    
    # Create virtual environment
    venv_command = "python -m venv venv"
    if not run_command(venv_command, cwd=backend_dir):
        print("❌ Failed to create virtual environment")
        return False
    
    # Determine activation script based on OS
    if platform.system() == "Windows":
        activate_script = os.path.join(backend_dir, "venv", "Scripts", "activate")
        pip_command = os.path.join(backend_dir, "venv", "Scripts", "pip")
        python_command = os.path.join(backend_dir, "venv", "Scripts", "python")
    else:
        activate_script = os.path.join(backend_dir, "venv", "bin", "activate")
        pip_command = os.path.join(backend_dir, "venv", "bin", "pip")
        python_command = os.path.join(backend_dir, "venv", "bin", "python")
    
    # Install dependencies
    install_command = f"{pip_command} install -r requirements.txt"
    if not run_command(install_command, cwd=backend_dir):
        print("❌ Failed to install backend dependencies")
        return False
    
    # Download spaCy model
    spacy_command = f"{python_command} -m spacy download en_core_web_sm"
    if not run_command(spacy_command, cwd=backend_dir):
        print("⚠️  Failed to download spaCy model (optional)")
    
    print("✅ Backend setup completed!")
    return True

def setup_frontend():
    """Setup React frontend"""
    print("\n🔧 Setting up Frontend (React)...")
    
    frontend_dir = os.path.join(os.getcwd(), 'frontend')
    
    # Install dependencies
    install_command = "npm install"
    if not run_command(install_command, cwd=frontend_dir):
        print("❌ Failed to install frontend dependencies")
        return False
    
    print("✅ Frontend setup completed!")
    return True

def create_start_scripts():
    """Create convenient start scripts"""
    print("\n📝 Creating start scripts...")
    
    # Backend start script
    if platform.system() == "Windows":
        backend_script = """@echo off
cd backend
call venv\\Scripts\\activate
python app.py
pause
"""
        with open("start_backend.bat", "w") as f:
            f.write(backend_script)
        
        # Frontend start script
        frontend_script = """@echo off
cd frontend
npm start
pause
"""
        with open("start_frontend.bat", "w") as f:
            f.write(frontend_script)
        
        print("✅ Created start_backend.bat and start_frontend.bat")
    
    else:
        # Unix-like systems
        backend_script = """#!/bin/bash
cd backend
source venv/bin/activate
python app.py
"""
        with open("start_backend.sh", "w") as f:
            f.write(backend_script)
        os.chmod("start_backend.sh", 0o755)
        
        frontend_script = """#!/bin/bash
cd frontend
npm start
"""
        with open("start_frontend.sh", "w") as f:
            f.write(frontend_script)
        os.chmod("start_frontend.sh", 0o755)
        
        print("✅ Created start_backend.sh and start_frontend.sh")

def main():
    """Main setup function"""
    print("🚀 PM Internship Recommendation Engine Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, "node")
        print(f"✅ Node.js found: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js is required but not found. Please install Node.js 16+")
        sys.exit(1)
    
    # Check npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, "npm")
        print(f"✅ npm found: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm is required but not found")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed")
        sys.exit(1)
    
    # Create start scripts
    create_start_scripts()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the backend server:")
    if platform.system() == "Windows":
        print("   - Double-click start_backend.bat")
        print("   - Or run: cd backend && venv\\Scripts\\activate && python app.py")
    else:
        print("   - Run: ./start_backend.sh")
        print("   - Or run: cd backend && source venv/bin/activate && python app.py")
    
    print("\n2. Start the frontend server (in a new terminal):")
    if platform.system() == "Windows":
        print("   - Double-click start_frontend.bat")
        print("   - Or run: cd frontend && npm start")
    else:
        print("   - Run: ./start_frontend.sh")
        print("   - Or run: cd frontend && npm start")
    
    print("\n3. Open your browser to: http://localhost:3000")
    print("\n🔗 Backend API will be available at: http://localhost:5000")

if __name__ == "__main__":
    main()
