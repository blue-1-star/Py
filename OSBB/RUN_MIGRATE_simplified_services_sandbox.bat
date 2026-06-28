@echo off
setlocal EnableExtensions
chcp 65001 >nul
title OSBB - Simplified Services Sandbox Migration

set "PROJECT=G:\Programming\Py\OSBB"
set "PYTHON=G:\Programming\Py\venv\Scripts\python.exe"
set "SCRIPT=%PROJECT%\MIGRATE_simplified_services_sandbox.py"

echo.
echo OSBB - Simplified paid-preorder services migration

echo This changes ONLY the live-services sandbox and creates a backup.
echo Stop the live-services sandbox bot before running this file.
echo.

if not exist "%PYTHON%" (
  echo [ERROR] Python not found: %PYTHON%
  pause
  exit /b 1
)
if not exist "%SCRIPT%" (
  echo [ERROR] Script not found: %SCRIPT%
  echo Copy the downloaded bundle contents directly to G:\Programming\Py\OSBB\
  pause
  exit /b 1
)

"%PYTHON%" "%SCRIPT%"
set "RESULT=%ERRORLEVEL%"
echo.
pause
exit /b %RESULT%
