@echo off
setlocal EnableExtensions

set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB phone-barrier access schema migration
echo This changes ONLY the live-services sandbox and creates a backup.
echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat before running this file.
echo.

"%PY%" "%ROOT%\MIGRATE_phone_barrier_access_sandbox.py"
echo.
pause
