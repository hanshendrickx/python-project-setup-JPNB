@echo off
setlocal enabledelayedexpansion

REM Prompt for project name
set /p PROJECT_NAME=Enter project name (default is JPNB_Sample): 
if "!PROJECT_NAME!"=="" set "PROJECT_NAME=JPNB_Sample"

REM Create and activate virtual environment
python -m venv env
call env\Scripts\activate

REM Install required packages and set up the environment
pip install -r requirements.txt
python setup_env.py

REM Run linting and formatting
ruff check .
black .

REM Run tests
pytest

REM Launch Jupyter Notebook
start "" jupyter notebook

REM Open VSCode in the current directory
code .

echo Setup complete. Jupyter Notebook is running in your browser and VSCode has been opened.