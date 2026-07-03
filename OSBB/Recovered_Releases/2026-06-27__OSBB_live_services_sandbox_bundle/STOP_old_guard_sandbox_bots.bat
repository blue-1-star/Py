@echo off
setlocal EnableExtensions
chcp 65001 >nul
title OSBB - Stop Old Guard Sandbox Bots

echo.
echo This stops only Python processes whose command line contains:
echo run_bot_guard_sandbox_v3.py --run
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$p = Get-CimInstance Win32_Process | Where-Object { ($_.Name -eq 'python.exe' -or $_.Name -eq 'pythonw.exe') -and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' }; if (-not $p) { Write-Host 'No old Guard Sandbox bot process was found.'; exit 0 }; $p | ForEach-Object { Write-Host ('Stopping PID ' + $_.ProcessId); Invoke-CimMethod -InputObject $_ -MethodName Terminate | Out-Null }; Write-Host 'Done.'"

echo.
pause
exit /b 0
