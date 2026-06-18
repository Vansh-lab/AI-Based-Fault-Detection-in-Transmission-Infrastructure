#!/usr/bin/env python3
"""
Quick Start Launcher for Transmission Line Fault Detection System
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("\n" + "="*70)
    print("🚀 AI-Based Fault Detection System - Quick Launcher")
    print("="*70 + "\n")
    
    # Get project root
    project_root = Path(__file__).parent
    app_path = project_root / "main.py"
    
    print("📋 System Check:")
    print(f"  ✓ Project directory: {project_root}")
    print(f"  ✓ App file: {app_path}")
    print(f"  ✓ Status: Ready to launch\n")
    
    print("🎯 Options:")
    print("  1. Run locally (Streamlit)")
    print("  2. Deploy to Streamlit Cloud")
    print("  3. View deployment guides\n")
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == "1":
        print("\n🔄 Starting Streamlit app...")
        print("   App will open at: http://localhost:8501\n")
        
        # Install dependencies silently
        print("📦 Checking dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", 
                       str(project_root / "requirements.txt")], 
                       cwd=str(project_root))
        
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", 
                       str(app_path), "--logger.level=error"],
                       cwd=str(project_root))
        
    elif choice == "2":
        print("\n📘 Streamlit Cloud Deployment:\n")
        print("""
1. Create account at https://share.streamlit.io
2. Push code to GitHub repository
3. Connect Streamlit Cloud to your GitHub repo
4. Click "Deploy" - that's it!

Your app will be available at: https://your-username-appname.streamlit.app

For detailed guide, see: QUICKSTART_ADVANCED_FEATURES.md
        """)
        
    elif choice == "3":
        print("\n📖 Available Deployment Guides:\n")
        guides = [
            ("QUICKSTART_ADVANCED_FEATURES.md", "Quick start & features"),
            ("EXECUTION_GUIDE.md", "How to run locally"),
            ("ADVANCED_FEATURES_COMPLETE.md", "Technical specifications"),
            ("FINAL_IMPLEMENTATION_SUMMARY.md", "Feature overview")
        ]
        
        for guide, description in guides:
            guide_path = project_root / guide
            if guide_path.exists():
                print(f"  ✓ {guide}")
                print(f"    └─ {description}\n")
        
        print("Open these files in your editor to read detailed guides.")
    
    else:
        print("Invalid option. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
