@echo off
setlocal EnableExtensions
chcp 65001 >nul
title OSBB - source_ref schema repair

set "PROJECT_ROOT=%~dp0"
set "PYTHON_EXE=%PROJECT_ROOT%..\venv\Scripts\python.exe"
set "SCRIPT=%PROJECT_ROOT%fix_source_ref_schema.py"

echo.
echo OSBB source_ref schema repair
echo.

if not exist "%SCRIPT%" (
    echo ERROR: %SCRIPT% was not found.
    echo Put both downloaded files directly into G:\Programming\Py\OSBB\
    echo.
    pause
    exit /b 1
)

if not exist "%PYTHON_EXE%" (
    echo ERROR: Python environment was not found:
    echo %PYTHON_EXE%
    echo.
    pause
    exit /b 1
)

"%PYTHON_EXE%" "%SCRIPT%"
set "RESULT=%ERRORLEVEL%"

echo.
if "%RESULT%"=="0" (
    echo Completed successfully.
) else (
    echo Repair was not completed. The log path is shown above.
)
echo.
pause
exit /b %RESULT%
