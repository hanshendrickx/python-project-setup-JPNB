@echo off
setlocal enabledelayedexpansion

if "%1"=="install" (
    pip install -r requirements.txt
) else if "%1"=="format" (
    black .
    ruff check . --fix
) else if "%1"=="lint" (
    ruff check .
    black . --check
) else if "%1"=="test" (
    pytest
) else if "%1"=="clean" (
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
    del /s /q *.pyc
    if exist .pytest_cache rd /s /q .pytest_cache
    if exist .ruff_cache rd /s /q .ruff_cache
) else (
    echo Usage: dev_tasks.bat [install^|format^|lint^|test^|clean]
)