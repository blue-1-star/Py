@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB profile confirmation READY-visibility check
echo Read-only check. No data will be changed.
echo.
"%PY%" "%ROOT%\CHECK_profile_confirmation_ready_visibility_fix.py"
echo.
pause
