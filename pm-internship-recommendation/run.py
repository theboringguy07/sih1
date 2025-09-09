#!python3
"""
Quick run script for PM Internship Recommendation Engine
Starts both backend and frontend servers without running setup
"""

import os
import sys

def main():
    """Run the setup.py with --run-only flag"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    setup_path = os.path.join(script_dir, "setup.py")
    
    # Execute setup.py with --run-only flag
    os.system(f"python \"{setup_path}\" --run-only")

if __name__ == "__main__":
    main()
