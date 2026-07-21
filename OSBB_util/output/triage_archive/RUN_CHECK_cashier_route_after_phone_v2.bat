@echo off
setlocal EnableExtensions

set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB live-services sandbox launcher check
echo This does not start Telegram polling.
echo.

"%PY%" "%ROOT%\run_bot_live_services_sandbox_v1.py"
echo.
pause
