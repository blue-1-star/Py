@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB two-barrier phone access - operational check
echo Read-only check.
echo.
"%PY%" "%ROOT%\CHECK_phone_barrier_access_operational_sandbox.py"
echo.
pause
