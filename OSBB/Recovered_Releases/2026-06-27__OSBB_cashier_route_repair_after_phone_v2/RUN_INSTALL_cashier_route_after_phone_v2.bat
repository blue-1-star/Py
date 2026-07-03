@echo off
setlocal EnableExtensions

set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB cashier-route repair after phone-access V2
echo Stop the sandbox bot with Ctrl+C before continuing.
echo.

"%PY%" "%ROOT%\INSTALL_cashier_route_after_phone_v2.py"
echo.
pause
