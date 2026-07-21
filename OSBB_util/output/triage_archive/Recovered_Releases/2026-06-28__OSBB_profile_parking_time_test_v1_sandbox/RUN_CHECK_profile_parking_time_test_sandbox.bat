@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB isolated parking_time TEST V1 - read-only check
echo.
"%PY%" "%ROOT%\CHECK_profile_parking_time_test_sandbox.py"
echo.
pause
