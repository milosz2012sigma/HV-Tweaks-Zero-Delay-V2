@echo off
title HV Tweaks - Zero Delay V2
color 0C
cls

echo ===============================================
echo.
echo   HV TWEAKS - ZERO DELAY V2
echo   Windows 11 Optimization Tool
echo.
echo ===============================================
echo.

echo Checking Python installation...
python --version >nul 2>&1

if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python found!
echo.

echo Installing/Checking dependencies...
pip install -r requirements.txt -q

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)

echo [OK] Dependencies ready!
echo.

echo Starting HV Tweaks application...
python main.py

pause