@echo off
title Navi Multitool - Installer
color 0b

echo ======================================================
echo           NAVI MULTITOOL INSTALLER
echo ======================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH.
    echo [!] Please install Python 3.8+ and try again.
    pause
    exit /b
)


echo [*] Installing dependencies from requirements.txt...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [!] Some dependencies failed to install.
    echo [!] Please check your internet connection or run as Administrator.
) else (
    echo.
    echo [+] Installation completed successfully!
    echo [+] You can now run the tool using start.bat or main.py
)

echo.
echo Press any key to exit...
pause >nul
