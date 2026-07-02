@echo off
setlocal EnableExtensions
chcp 65001 >nul
title OSBB - Live Services Sandbox

set "PROJECT=G:\Programming\Py\OSBB"
set "PYTHON=G:\Programming\Py\venv\Scripts\python.exe"
set "SCRIPT=%PROJECT%\run_bot_live_services_sandbox_v1.py"

echo.
echo OSBB LIVE SERVICES SANDBOX
echo Database: osbb_test_live_services_2026-06-26_20-13-26.db
echo.

if not exist "%PYTHON%" (
    echo [ERROR] Python was not found:
    echo %PYTHON%
    echo.
    pause
    exit /b 1
)

if not exist "%SCRIPT%" (
    echo [ERROR] Launcher was not found:
    echo %SCRIPT%
    echo.
    echo Extract the supplied archive directly into:
    echo G:\Programming\Py\OSBB\
    echo.
    pause
    exit /b 1
)

"%PYTHON%" "%SCRIPT%" --run
set "RESULT=%ERRORLEVEL%"

echo.
if "%RESULT%"=="2" (
    echo Old Guard Sandbox bot windows are still running.
    echo Use STOP_old_guard_sandbox_bots.bat from this bundle, then start again.
)
echo.
pause
exit /b %RESULT%
