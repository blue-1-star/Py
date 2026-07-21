@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB profile confirmation READY-visibility fix
echo Stop the sandbox bot with Ctrl+C before continuing.
echo.
"%PY%" "%ROOT%\INSTALL_profile_confirmation_ready_visibility_fix.py"
echo.
pause
