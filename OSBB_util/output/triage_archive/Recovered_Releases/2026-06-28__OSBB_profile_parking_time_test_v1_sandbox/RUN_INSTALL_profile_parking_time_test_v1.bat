@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB isolated parking_time TEST V1 - source installation
echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat with Ctrl+C first.
echo.
"%PY%" "%ROOT%\INSTALL_profile_parking_time_test_v1.py"
echo.
pause
