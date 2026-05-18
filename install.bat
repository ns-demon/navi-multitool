@echo off
title Navi Multitool - Installer
color 0b

echo ======================================================
echo           NAVI MULTITOOL INSTALLER
echo ======================================================
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto python_found
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto python_found
)

color 0c
echo ======================================================
echo             ERROR: PYTHON NOT FOUND
echo ======================================================
echo.
echo Python is not installed or not in PATH (environment variable).
echo.
echo Solution:
echo 1. Download Python: https://www.python.org/downloads/
echo 2. Run the installer.
echo 3. IMPORTANT: Check the box at the bottom:
echo    "Add python.exe to PATH" (or "Add Python to PATH")
echo 4. Click "Install Now".
echo 5. Restart this installer.
echo.
echo ======================================================
echo.
pause
exit /b

:python_found
echo [+] Python found (%PYTHON_CMD%)
echo.

%PYTHON_CMD% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Pip is not available. Trying to install/restore pip...
    %PYTHON_CMD% -m ensurepip --default-pip >nul 2>&1
    
    %PYTHON_CMD% -m pip --version >nul 2>&1
    if %errorlevel% neq 0 (
        color 0c
        echo ======================================================
        echo               ERROR: PIP NOT FOUND
        echo ======================================================
        echo.
        echo The Python Package Manager (pip) was not found.
        echo.
        echo Solution:
        echo 1. Open Command Prompt (cmd) as Administrator.
        echo 2. Run the following command to manually install pip:
        echo    %PYTHON_CMD% -m ensurepip --default-pip
        echo 3. Restart this installer.
        echo.
        echo ======================================================
        echo.
        pause
        exit /b
    )
)

echo [*] Installing dependencies from requirements.txt...
%PYTHON_CMD% -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    color 0c
    echo.
    echo [!] Some dependencies failed to install.
    echo [!] Please check your internet connection or run as Administrator.
    echo.
    echo If this error persists, you can try installing the packages manually by
    echo running this in cmd:
    echo %PYTHON_CMD% -m pip install -r requirements.txt
) else (
    echo.
    echo [+] Installation completed successfully!
    echo [+] You can now run the tool using start.bat or main.py
)

echo.
echo Press any key to exit...
pause >nul
