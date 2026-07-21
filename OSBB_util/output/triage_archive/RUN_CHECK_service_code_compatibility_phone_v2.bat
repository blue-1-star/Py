@echo off
setlocal EnableExtensions

set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB service-code compatibility check
echo Read-only check. No data will be changed.
echo.

"%PY%" "%ROOT%\CHECK_service_code_compatibility_phone_v2.py"
echo.
pause
