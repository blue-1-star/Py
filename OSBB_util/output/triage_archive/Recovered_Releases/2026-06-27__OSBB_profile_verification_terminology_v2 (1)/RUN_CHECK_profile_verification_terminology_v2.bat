@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB profile verification terminology/readiness V2 check
echo Read-only check. No data will be changed.
echo.
"%PY%" "%ROOT%\CHECK_profile_verification_terminology_v2.py"
echo.
pause
