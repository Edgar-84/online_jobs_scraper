@echo off

if not exist "venv" (
    echo Creating virtual environment for scraper...
    python -m venv venv

    call venv\Scripts\activate.bat

    if exist "requirements.txt" (
        echo Installing dependencies from requirements.txt...
        pip install -r requirements.txt
    ) else (
        echo Warning: requirements.txt not found
    )
) else (
    REM Virtual environment already exists.
    call venv\Scripts\activate.bat
)

if exist "main.py" (
    start /min python main.py

) else (
    echo Error: main.py not found in the src directory
)

