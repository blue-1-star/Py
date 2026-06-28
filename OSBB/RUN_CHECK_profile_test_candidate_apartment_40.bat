@echo off
setlocal EnableExtensions

set "ROOT=G:\Programming\Py\OSBB"
set "PY=G:\Programming\Py\venv\Scripts\python.exe"

echo OSBB apartment 40 profile-verification test preflight
echo Read-only: no data will be changed.
echo.

"%PY%" "%ROOT%\CHECK_profile_test_candidate_apartment_40.py" --apartment 40
echo.
pause
