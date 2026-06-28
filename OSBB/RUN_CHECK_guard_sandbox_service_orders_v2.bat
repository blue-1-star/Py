@echo off
setlocal EnableExtensions
chcp 65001 >nul
title OSBB - Guard Sandbox Diagnosis V2

set "PROJECT=G:\Programming\Py\OSBB"
set "PYTHON=G:\Programming\Py\venv\Scripts\python.exe"
set "SCRIPT=%PROJECT%\CHECK_guard_sandbox_service_orders_v2.py"

echo.
echo OSBB Guard Sandbox - Service Orders Diagnosis V2
echo This is read-only: no bot code and no database will be changed.
echo.

if not exist "%PYTHON%" (
    echo [ERROR] Python was not found:
    echo %PYTHON%
    echo.
    pause
    exit /b 1
)

if not exist "%SCRIPT%" (
    echo [ERROR] The diagnosis script was not found:
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
