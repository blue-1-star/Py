@echo off
setlocal EnableExtensions
chcp 65001 >nul
title OSBB - Retire Legacy New Remote Sandbox Tests
set "PROJECT=G:\Programming\Py\OSBB"
set "PYTHON=G:\Programming\Py\venv\Scripts\python.exe"
set "SCRIPT=%PROJECT%\RETIRE_legacy_new_remote_test_orders_sandbox.py"
echo.
echo Retires only unpaid old TEST new-remote sandbox orders.
echo It does not delete history and creates a backup.
echo Stop the live-services sandbox bot first.
echo.
"%PYTHON%" "%SCRIPT%"
pause
