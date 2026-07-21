@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB profile critical-codes repair check
echo Read-only check. No data will be changed.
echo.
"%PY%" "%ROOT%\CHECK_profile_critical_codes_fix.py"
echo.
pause
