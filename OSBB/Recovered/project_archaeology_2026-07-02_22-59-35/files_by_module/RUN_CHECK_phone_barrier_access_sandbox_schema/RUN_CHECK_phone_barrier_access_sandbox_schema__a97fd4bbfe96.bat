@echo off
setlocal EnableExtensions

set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB phone-barrier access sandbox schema check
echo Read-only check. No data will be changed.
echo.

"%PY%" "%ROOT%\CHECK_phone_barrier_access_sandbox_schema.py"
echo.
pause
