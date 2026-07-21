@echo off
setlocal EnableExtensions

set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB phone-access UI fix — reliable installer
echo.
echo Before continuing, stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat with Ctrl+C.
echo.
"%PY%" "%~dp0INSTALL_PHONE_ACCESS_UI_FIX_v2.py" --root "%ROOT%" --python "%PY%"
echo.
pause
