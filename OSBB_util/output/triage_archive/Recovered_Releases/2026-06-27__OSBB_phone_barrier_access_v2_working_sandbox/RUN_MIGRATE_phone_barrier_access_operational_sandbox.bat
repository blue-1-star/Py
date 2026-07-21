@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB two-barrier phone access - operational migration
echo SANDBOX ONLY. Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat first.
echo.
"%PY%" "%ROOT%\MIGRATE_phone_barrier_access_operational_sandbox.py"
echo.
pause
