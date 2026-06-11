@echo off
pushd "%~dp0"
:: ========================================================
::              CODEX COC FARM - RUNNER
::           Created & Maintained by zsxbb
:: ========================================================
title CODEX COC FARM
color 0b

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ========================================================
    echo  [!] ERROR: Python not found in your PATH.
    echo  Please install Python and check 'Add Python to Path'
    echo ========================================================
    pause
    exit
)

:: Auto Install/Update Requirements (Runs Once)
set "VENV_DIR=%~dp0codex_venv"

if not exist "%VENV_DIR%" (
    echo ========================================================
    echo  [!] INITIAL SETUP & INSTALLATION
    echo ========================================================
    echo  This script will create a local virtual environment:
    echo  Folder: \codex_venv\
    echo.
    echo  It will install the following Python libraries:
    echo  - pyautogui, opencv-python, numpy
    echo  - python-imagesearch, pygetwindow, pynput
    echo.
    echo  [HOW TO UNINSTALL]:
    echo  Simply delete the 'codex_venv' folder to remove all
    echo  installed libraries and the environment.
    echo ========================================================
    set /p "install_choice=Install requirements now? (Y/N): "
    if /i not "%install_choice%"=="Y" (
        echo [!] Installation cancelled. Some features may not work.
        pause
        goto menu
    )
    
    echo [CODEX] Creating virtual environment: codex_venv...
    python -m venv codex_venv
    
    echo [CODEX] Installing Requirements...
    "%VENV_DIR%\Scripts\pip.exe" install -r "requirements.txt"
    echo [CODEX] Environment initialized successfully!
    echo.
)

set "PYTHON_EXEC=%VENV_DIR%\Scripts\python.exe"
if not exist "%PYTHON_EXEC%" (
    set "PYTHON_EXEC=python"
)

:menu

cls
echo ========================================================
echo.
echo           C O D E X   C O C   F A R M
echo.
echo ========================================================
echo.
echo  [1] START BOT (scripts/autoattack.py)
echo  [2] RECORD SPAWN POINTS (scripts/get_spawn.py)
echo  [3] EXIT
echo.
echo ========================================================
set /p choice=" > Selection: "

if "%choice%"=="1" goto run_bot
if "%choice%"=="2" goto run_spawn
if "%choice%"=="3" goto end
goto menu

:run_bot
echo.
if not exist "scripts/autoattack.py" (
    echo [ERROR] scripts/autoattack.py not found.
    pause
    goto menu
)
echo [CODEX] Starting Bot (Effective Mode)...
"%PYTHON_EXEC%" "scripts/autoattack.py"
echo [CODEX] Attack cycle finished. Restarting fresh...
timeout /t 3 >nul
goto run_bot

:run_spawn
echo.
if not exist "scripts/get_spawn.py" (
    echo [ERROR] scripts/get_spawn.py not found.
    pause
    goto menu
)
echo [CODEX] Starting Spawn Point Recorder...
"%PYTHON_EXEC%" "scripts/get_spawn.py"
echo.
pause
goto menu

:end
popd
exit
