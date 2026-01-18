@echo off
echo Training Transmission Line Fault Detection Model...
echo.
echo Prerequisites:
echo - Dataset organized in dataset/train, dataset/val folders
echo - Dependencies installed: pip install -r requirements.txt
echo.
timeout /t 2

cd src
python train.py
cd ..

echo.
echo Training completed! Check models/ directory for saved model.
pause
