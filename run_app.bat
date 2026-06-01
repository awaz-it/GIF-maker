@echo off
echo ====================================
echo WAZ GIF Maker Pro - Desktop App
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

echo Checking dependencies...
pip show PyQt5 >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Dependencies OK!
)

echo.
echo Starting GIF Maker Pro...
echo.
python gif_maker_app.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    pause
)
