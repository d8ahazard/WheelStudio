@echo off
setlocal enabledelayedexpansion

REM Detect Python executable
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python not found! Please install Python 3.8 or newer.
    exit /b 1
)

REM Set CUDA_HOME if it's not set but CUDA is installed
if not defined CUDA_HOME (
    for /D %%i in ("C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v*.*") do (
        if exist "%%i\bin\nvcc.exe" (
            set "CUDA_HOME=%%i"
            echo Set CUDA_HOME to !CUDA_HOME!
            goto cuda_home_set
        )
    )
    
    for /D %%i in ("C:\NVIDIA\CUDA\v*.*") do (
        if exist "%%i\bin\nvcc.exe" (
            set "CUDA_HOME=%%i"
            echo Set CUDA_HOME to !CUDA_HOME!
            goto cuda_home_set
        )
    )
)

:cuda_home_set
REM Ensure there's a build virtual environment
if not exist "build_venv" (
    echo Creating build virtual environment...
    python -m venv build_venv
)

REM Activate virtual environment and install pip-tools
call build_venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install build pip-tools

REM Parse arguments
set package=
set flag=

:parse_args
if "%~1"=="" goto :end_parse_args
if /i "%~1"=="--package" (
    set package=%~2
    shift
) else if /i "%~1"=="--no-isolation" (
    set flag=--no-isolation
)
shift
goto :parse_args

:end_parse_args
echo.
echo Checking for CUDA support...
where nvidia-smi >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo CUDA detected! Installing PyTorch with CUDA support...
    pip install torch>=2.4.0 torchvision>=0.19.0 torchaudio>=2.4.0 --index-url https://download.pytorch.org/whl/cu124
) else (
    echo CUDA not detected. Installing CPU version of PyTorch...
    pip install torch>=2.4.0 torchvision>=0.19.0 torchaudio>=2.4.0
)

:: Create wheels directory
if not exist wheels mkdir wheels

REM Run the build script
if not "%package%"=="" (
    echo Building only package: %package%, CUDA_HOME: %CUDA_HOME%
    python build_wheels.py --package %package% %flag% --cuda-home "%CUDA_HOME%"
) else (
    echo Building all packages, CUDA_HOME: %CUDA_HOME%
    python build_wheels.py %flag% --cuda-home "%CUDA_HOME%"
)

echo.
echo Build completed! Check the wheels directory for built wheels.
endlocal


if errorlevel 1 (
    echo Error building wheels. Check the output above.
    call build_venv\Scripts\deactivate
    exit /b 1
)

:: Deactivate venv
call build_venv\Scripts\deactivate

echo.
echo All wheels have been built and collected in the wheels directory.
echo You can install them with: pip install wheels\*.whl
echo.
pause 