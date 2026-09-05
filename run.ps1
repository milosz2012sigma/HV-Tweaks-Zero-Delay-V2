# HV Tweaks - PowerShell Launcher
# Run with: powershell -ExecutionPolicy Bypass -File run.ps1

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host " " -ForegroundColor Cyan
Write-Host "   HV TWEAKS - ZERO DELAY V2" -ForegroundColor Cyan
Write-Host "   Windows 11 Optimization Tool" -ForegroundColor Cyan
Write-Host " " -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host " " -ForegroundColor Cyan

Write-Host "Checking Python installation..." -ForegroundColor Yellow

try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host " " -ForegroundColor White
Write-Host "Installing/Checking dependencies..." -ForegroundColor Yellow

pip install -r requirements.txt -q

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Dependencies ready!" -ForegroundColor Green
Write-Host " " -ForegroundColor White

Write-Host "Starting HV Tweaks application..." -ForegroundColor Yellow
Write-Host " " -ForegroundColor White

python main.py

Read-Host "Press Enter to exit"