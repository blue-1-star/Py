@echo off
setlocal EnableExtensions
set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB two-barrier phone access - code installation
echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat before continuing.
echo This step changes source files only and makes a source-code backup.
echo.
"%PY%" "%ROOT%\INSTALL_phone_barrier_access_v2.py"
echo.
pause
