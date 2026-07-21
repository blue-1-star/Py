@echo off
setlocal EnableExtensions
chcp 65001 >nul
title OSBB - Guard Sandbox Service Orders Diagnosis

set "PROJECT=G:\Programming\Py\OSBB"
set "PYTHON=%PROJECT%\..\venv\Scripts\python.exe"
set "SCRIPT=%PROJECT%\CHECK_guard_sandbox_service_orders.py"

echo.
echo OSBB Guard Sandbox - Service Orders Diagnosis
echo This check is read-only. It does not alter the bot, database, or config.
echo.

if not exist "%PYTHON%" (
    echo [ERROR] Python was not found:
    echo %PYTHON%
    echo.
    pause
    exit /b 1
)

if not exist "%SCRIPT%" (
    echo [ERROR] Diagnosis script was not found:
    echo %SCRIPT%
    echo.
    echo Put this BAT and CHECK_guard_sandbox_service_orders.py
    echo directly into G:\Programming\Py\OSBB\
    echo.
    pause
    exit /b 1
)

"%PYTHON%" "%SCRIPT%"
set "RESULT=%ERRORLEVEL%"

echo.
if not "%RESULT%"=="0" (
    echo The diagnosis reported an error. Attach its text report anyway.
)
echo.
pause
exit /b %RESULT%
