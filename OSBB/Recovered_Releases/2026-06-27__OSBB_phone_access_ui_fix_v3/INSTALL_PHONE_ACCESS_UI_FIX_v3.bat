@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB phone-access UI fix v3
echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat with Ctrl+C first.
echo.
"%PY%" "%~dp0INSTALL_PHONE_ACCESS_UI_FIX_v3.py" --root "%ROOT%" --python "%PY%"
echo.
pause
