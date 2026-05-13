@echo off
title Navi Multitool
echo Loading Navi...
python main.py
if %errorlevel% neq 0 (
    echo.
    echo [!] Navi crashed or exited with an error (Code: %errorlevel%)
    echo [!] Possible causes: Missing libraries, Python not in PATH, or code error.
    echo [!] Try running 'install.bat' to fix library issues or open a ticket in the server.
    echo.
    pause
)
