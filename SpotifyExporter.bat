@echo off
setlocal

echo Checking if Python is installed...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not found in the PATH.
    echo Please install Python before running this script.
    pause
    exit /b 1
) else (
    python --version
)

echo Checking if pip is installed...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"

    if not exist get-pip.py (
        echo ERROR: Failed to download get-pip.py. Please check your internet connection.
        pause
        exit /b 1
    )

    python get-pip.py
    pip --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Pip installation failed. Please try to install pip manually.
        pause
        exit /b 1
    )

    del get-pip.py >nul 2>&1
) else (
    pip --version
)

echo Checking if keyring is installed...
python -c "import keyring" >nul 2>&1
if %errorlevel% neq 0 (
    pip install keyring
)

echo Checking if spotipy is installed...
python -c "import spotipy" >nul 2>&1
if %errorlevel% neq 0 (
    pip install spotipy
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install spotipy. Please check your internet connection.
        pause
        exit /b 1
)

echo Checking if requests is installed...
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    pip install requests
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install requests. Please check your internet connection.
        pause
        exit /b 1
)

cd /d "%~dp0"
python SpotifyExporter.py
if %errorlevel% neq 0 (
    echo ERROR: There was an issue running SpotifyExporter.py.
    pause
    exit /b 1
)

echo Export completed! Opening folder..
echo .
start "" "%~dp0Exports"

pause
