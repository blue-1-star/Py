@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB profile verification terminology/readiness V2
echo Stop the sandbox bot with Ctrl+C before continuing.
echo.
"%PY%" "%ROOT%\INSTALL_profile_verification_terminology_v2.py"
echo.
pause
