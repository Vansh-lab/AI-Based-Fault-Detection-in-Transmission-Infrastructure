@echo off
echo Starting Transmission Line Fault Detector Application...
echo.
echo Make sure you have:
echo 1. Installed dependencies: pip install -r requirements.txt
echo 2. Trained the model: python src/train.py
echo.
timeout /t 2

streamlit run app/main.py
pause
