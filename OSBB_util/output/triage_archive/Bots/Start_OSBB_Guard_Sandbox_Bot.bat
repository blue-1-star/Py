@echo off
setlocal EnableExtensions

rem ================================================================
rem OSBB — отдельный запуск guard sandbox-бота
rem Откройте этот .bat двойным щелчком: VS Code останется свободным.
rem Остановить бота: в отдельном окне нажмите Ctrl+C.
rem ================================================================

set "PROJECT=G:\Programming\Py\OSBB"
set "PYTHON=G:\Programming\Py\venv\Scripts\python.exe"
set "RUNNER=%PROJECT%\run_bot_guard_sandbox_v2.py"
set "SANDBOX=%PROJECT%\Data\db\sandbox\osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09.db"

if not exist "%PYTHON%" (
    echo [ERROR] Не найден Python:
    echo %PYTHON%
    pause
    exit /b 1
)

if not exist "%RUNNER%" (
    echo [ERROR] Не найден launcher:
    echo %RUNNER%
    pause
    exit /b 1
)

if not exist "%SANDBOX%" (
    echo [ERROR] Не найдена guard sandbox-БД:
    echo %SANDBOX%
    pause
    exit /b 1
)

echo Запускаю отдельное окно: OSBB Guard Sandbox Bot
echo Не запускайте одновременно обычный бот: Telegram не даст двум экземплярам получать обновления.
start "OSBB Guard Sandbox Bot" cmd.exe /k ""%PYTHON%" "%RUNNER%" --sandbox "%SANDBOX%" --run"

endlocal
