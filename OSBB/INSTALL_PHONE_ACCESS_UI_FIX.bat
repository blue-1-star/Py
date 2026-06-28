@echo off
setlocal EnableExtensions

echo OSBB phone-access UI fix
echo.
echo Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat with Ctrl+C before continuing.
echo This installer replaces only Bots\handlers\service_orders_workspace.py.
echo.

set "ROOT=G:\Programming\Py\OSBB"
set "SRC=%~dp0Bots\handlers\service_orders_workspace.py"
set "DST=%ROOT%\Bots\handlers\service_orders_workspace.py"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

if not exist "%SRC%" (
  echo ERROR: replacement source is missing:
  echo %SRC%
  pause
  exit /b 1
)

if not exist "%DST%" (
  echo ERROR: current workspace file is missing:
  echo %DST%
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$dst=$env:DST; $stamp=Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'; Copy-Item -LiteralPath $dst -Destination ($dst + '.before_phone_access_ui_fix_' + $stamp) -Force"

copy /Y "%SRC%" "%DST%" >nul
if errorlevel 1 (
  echo ERROR: could not replace the workspace file.
  pause
  exit /b 1
)

"%PY%" -m py_compile "%DST%"
if errorlevel 1 (
  echo ERROR: syntax check failed. Restore the .before_phone_access_ui_fix_ backup.
  pause
  exit /b 1
)

echo.
echo SUCCESS: phone-access workspace installed.
echo Backup of previous file was created beside it.
pause
