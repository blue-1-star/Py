@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB isolated parking_time TEST V1 - sandbox migration
echo Only dedicated TEST tables will be created.
echo.
"%PY%" "%ROOT%\MIGRATE_profile_parking_time_test_sandbox.py"
echo.
pause
