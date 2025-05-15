@echo off
setlocal

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in the PATH.
    echo Please install Python 3.6 or higher.
    pause
    exit /b 1
)

REM Run the Python script with all arguments passed to this batch file
python manage_submodules.py %*

if %ERRORLEVEL% NEQ 0 (
    echo An error occurred while running the script.
    pause
)

endlocal 