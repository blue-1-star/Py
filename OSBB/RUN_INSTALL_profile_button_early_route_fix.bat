@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB profile button early-route repair
echo Stop the sandbox bot with Ctrl+C before continuing.
echo.
"%PY%" "%ROOT%\INSTALL_profile_button_early_route_fix.py"
echo.
pause
