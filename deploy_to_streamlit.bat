@echo off
REM Streamlit Cloud Deployment Helper Script
REM Run this to help setup Git and deployment

echo.
echo ================================
echo Streamlit Cloud Deployment Setup
echo ================================
echo.
echo This script will help you deploy to Streamlit Cloud
echo.

REM Check if Git is installed
echo Checking for Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Git is NOT installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo Then run this script again.
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Git is installed!
    git --version
)

echo.
echo ================================
echo STEP 1: Configure Git (First Time Only)
echo ================================
echo.
set /p gitname="Enter your name (for Git commits): "
set /p gitemail="Enter your email (for Git commits): "

git config --global user.name "%gitname%"
git config --global user.email "%gitemail%"

echo ✅ Git configured!

echo.
echo ================================
echo STEP 2: Initialize Repository
echo ================================
echo.

REM Check if already a git repo
if exist .git (
    echo ✅ Repository already initialized
) else (
    echo Initializing Git repository...
    git init
    echo ✅ Repository initialized
)

echo.
echo ================================
echo STEP 3: Add Files & Commit
echo ================================
echo.

git add .
git commit -m "Transmission Fault Detection - Ready for Deployment"

echo ✅ Files committed!

echo.
echo ================================
echo STEP 4: Next Steps
echo ================================
echo.
echo Now you need to:
echo.
echo 1. Create a GitHub account (if you don't have one):
echo    https://github.com/signup
echo.
echo 2. Create a new repository on GitHub:
echo    https://github.com/new
echo    Name it: transmission-fault-detection
echo    Make it PUBLIC
echo.
echo 3. After creating, GitHub will show you commands like:
echo    git remote add origin https://github.com/YOUR-USERNAME/transmission-fault-detection.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Copy and paste those commands here
echo.
echo 5. Then sign up on Streamlit Cloud:
echo    https://share.streamlit.io
echo.
echo 6. Deploy from Streamlit Cloud dashboard!
echo.
echo ================================
echo Full Deployment Guide:
echo ================================
echo.
echo Read: STREAMLIT_CLOUD_DEPLOYMENT.md
echo.
pause
