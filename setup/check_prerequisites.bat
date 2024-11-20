@echo off
setlocal enabledelayedexpansion

echo Checking prerequisites...

REM Check if running on Windows
ver | find "Windows" > nul
if errorlevel 1 (
    echo This script is designed for Windows only.
    exit /b 1
)

REM Check for Python installation
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    exit /b 1
)

REM Check Python version
for /f "tokens=2 delims=." %%a in ('python --version 2^>^&1') do set python_major=%%a
if %python_major% lss 8 (
    echo Python version 3.8 or higher is required.
    echo Current version: 
    python --version
    exit /b 1
)

REM Check for pip installation
pip --version > nul 2>&1
if errorlevel 1 (
    echo pip is not installed or not in PATH.
    echo Please ensure pip is installed with your Python installation.
    exit /b 1
)

REM Check for Git installation
git --version > nul 2>&1
if errorlevel 1 (
    echo Git is not installed or not in PATH.
    echo Please install Git from https://git-scm.com/download/win
    exit /b 1
)

echo All prerequisites are met.
exit /b 0