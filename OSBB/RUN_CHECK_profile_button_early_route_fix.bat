@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB profile button early-route check
echo Read-only. Telegram polling will not start and no database data will change.
echo.
"%PY%" "%ROOT%\CHECK_profile_button_early_route_fix.py"
echo.
pause
