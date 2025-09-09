#!python3
"""
Setup script for PM Internship Recommendation Engine
Automates the setup process for both backend and frontend
"""

import os
import sys
import subprocess
import platform
import threading
import time
import signal
import argparse
from pathlib import Path

# Ensure UTF-8 output on Windows consoles to avoid UnicodeEncodeError with emojis
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

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

def start_servers():
    """Start both backend and frontend servers concurrently"""
    print("\n🚀 Starting servers...")
    
    backend_dir = os.path.join(os.getcwd(), 'backend')
    frontend_dir = os.path.join(os.getcwd(), 'frontend')
    
    # Prepare commands based on OS
    if platform.system() == "Windows":
        backend_python = os.path.join(backend_dir, "venv", "Scripts", "python.exe")
        backend_cmd = [backend_python, "app.py"]
        frontend_cmd = ["cmd", "/c", "npm", "start"]
    else:
        backend_python = os.path.join(backend_dir, "venv", "bin", "python")
        backend_cmd = [backend_python, "app.py"]
        frontend_cmd = ["npm", "start"]
    
    # Global variables to store process references
    global backend_process, frontend_process
    backend_process = None
    frontend_process = None
    
    def start_backend():
        """Start the Flask backend server"""
        global backend_process
        try:
            print("🔧 Starting Flask backend server...")
            backend_process = subprocess.Popen(
                backend_cmd,
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Wait a moment for the server to start
            time.sleep(3)
            
            if backend_process.poll() is None:
                print("✅ Backend server started successfully on http://localhost:5000")
            else:
                stdout, stderr = backend_process.communicate()
                print(f"❌ Backend server failed to start")
                print(f"Error: {stderr}")
                
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
    
    def start_frontend():
        """Start the React frontend server"""
        global frontend_process
        try:
            print("🔧 Starting React frontend server...")
            # Wait for backend to be ready
            time.sleep(5)
            
            frontend_process = subprocess.Popen(
                frontend_cmd,
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Wait a moment for the server to start
            time.sleep(8)
            
            if frontend_process.poll() is None:
                print("✅ Frontend server started successfully on http://localhost:3000")
            else:
                stdout, stderr = frontend_process.communicate()
                print(f"❌ Frontend server failed to start")
                print(f"Error: {stderr}")
                
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
    
    def signal_handler(signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n🛑 Shutting down servers...")
        
        if backend_process and backend_process.poll() is None:
            print("🔧 Stopping backend server...")
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
                print("✅ Backend server stopped")
            except subprocess.TimeoutExpired:
                backend_process.kill()
                print("🔨 Backend server force killed")
        
        if frontend_process and frontend_process.poll() is None:
            print("🔧 Stopping frontend server...")
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=5)
                print("✅ Frontend server stopped")
            except subprocess.TimeoutExpired:
                frontend_process.kill()
                print("🔨 Frontend server force killed")
        
        print("\n👋 Goodbye!")
        sys.exit(0)
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)
    
    # Start servers in separate threads
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    
    backend_thread.start()
    frontend_thread.start()
    
    # Wait for threads to complete startup
    backend_thread.join()
    frontend_thread.join()
    
    # Keep the main thread alive and monitor servers
    print("\n🎉 Both servers are running!")
    print("\n📋 Access your application:")
    print("   🌐 Frontend: http://localhost:3000")
    print("   🔗 Backend API: http://localhost:5000")
    print("\n💡 Press Ctrl+C to stop both servers")
    print("\n" + "="*50)
    
    try:
        while True:
            # Check if both processes are still running
            if backend_process and backend_process.poll() is not None:
                print("❌ Backend server has stopped unexpectedly")
                break
            if frontend_process and frontend_process.poll() is not None:
                print("❌ Frontend server has stopped unexpectedly")
                break
            time.sleep(2)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(
        description='Setup PM Internship Recommendation Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python setup.py              # Setup and ask to start servers
  python setup.py --start      # Setup and automatically start servers
  python setup.py --no-start   # Setup only, don't start servers
  python setup.py --run-only   # Skip setup, just start servers'''
    )
    
    parser.add_argument('--start', action='store_true',
                       help='Automatically start servers after setup')
    parser.add_argument('--no-start', action='store_true',
                       help='Setup only, do not start servers')
    parser.add_argument('--run-only', action='store_true',
                       help='Skip setup, just start the servers')
    
    args = parser.parse_args()
    
    print("🚀 PM Internship Recommendation Engine Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Handle run-only mode
    if args.run_only:
        print("\n🏃‍♂️ Running servers without setup...")
        start_servers()
        return
    
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
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, shell=True)
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
    
    # Handle server starting based on arguments
    if args.start:
        # Automatically start servers
        start_servers()
    elif args.no_start:
        # Don't start servers, just show instructions
        print("\n📋 To start the application later:")
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
    else:
        # Ask user if they want to start the servers automatically
        print("\n🚀 Would you like to start the application now? (Y/n): ", end="")
        try:
            response = input().strip().lower()
            if response == '' or response == 'y' or response == 'yes':
                start_servers()
            else:
                print("\n📋 To start the application later:")
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
                print("\n💡 Next time, use 'python setup.py --start' to skip this prompt")
        except KeyboardInterrupt:
            print("\n\n👋 Setup completed. Run this script again to start the servers.")
            sys.exit(0)

if __name__ == "__main__":
    main()
