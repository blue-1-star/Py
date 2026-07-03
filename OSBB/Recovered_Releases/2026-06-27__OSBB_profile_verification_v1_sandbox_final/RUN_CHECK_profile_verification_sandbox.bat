@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"
echo OSBB resident profile verification V1 - sandbox check
echo Read-only check. No data will be changed.
echo.
"%PY%" "%ROOT%\CHECK_profile_verification_sandbox.py"
echo.
pause
