@echo off
setlocal EnableExtensions
chcp 65001 >nul
title OSBB - Find Actual Service Order State

set "PROJECT=G:\Programming\Py\OSBB"
set "PYTHON=G:\Programming\Py\venv\Scripts\python.exe"
set "SCRIPT=%PROJECT%\FIND_actual_service_order_state.py"

echo.
echo OSBB - Find Actual Service Order State
echo Read-only: this does not change databases, source files, or bot processes.
echo.

if not exist "%PYTHON%" (
    echo [ERROR] Python was not found:
    echo %PYTHON%
    echo.
    pause
    exit /b 1
)

if not exist "%SCRIPT%" (
    echo [ERROR] Script was not found:
    echo %SCRIPT%
    echo.
    echo Put both downloaded files directly in:
    echo G:\Programming\Py\OSBB\
    echo.
    pause
    exit /b 1
)

"%PYTHON%" "%SCRIPT%"
set "RESULT=%ERRORLEVEL%"

echo.
pause
exit /b %RESULT%
