@echo off
setlocal EnableExtensions
chcp 65001 >nul
title OSBB - Live Services Sandbox Payment Schema Fix

set "PROJECT=G:\Programming\Py\OSBB"
set "PYTHON=G:\Programming\Py\venv\Scripts\python.exe"
set "SCRIPT=%PROJECT%\FIX_live_services_sandbox_payment_schema.py"

echo.
echo OSBB LIVE SERVICES SANDBOX - PAYMENT SCHEMA FIX
echo.
echo IMPORTANT:
echo 1. Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat first with Ctrl+C.
echo 2. This repair changes only the live-services SANDBOX database.
echo 3. A backup will be created automatically.
echo.

if not exist "%PYTHON%" (
    echo [ERROR] Python was not found:
    echo %PYTHON%
    pause
    exit /b 1
)

if not exist "%SCRIPT%" (
    echo [ERROR] Script was not found:
    echo %SCRIPT%
    echo Put this BAT and FIX_live_services_sandbox_payment_schema.py
    echo directly into G:\Programming\Py\OSBB\
    pause
    exit /b 1
)

"%PYTHON%" "%SCRIPT%"
set "RESULT=%ERRORLEVEL%"

echo.
if "%RESULT%"=="0" (
    echo Repair completed successfully.
) else (
    echo Repair was not completed. Read the log path above.
)
echo.
pause
exit /b %RESULT%
