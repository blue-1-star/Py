@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"
echo OSBB resident profile verification V1 - sandbox migration
echo This changes ONLY the live-services sandbox database and creates a backup.
echo.
"%PY%" "%ROOT%\MIGRATE_profile_verification_sandbox.py"
echo.
pause
