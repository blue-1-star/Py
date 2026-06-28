@echo off
setlocal EnableExtensions

rem Создан автоматически: чистая live sandbox для услуг / пультов.
rem Остановить бота: Ctrl+C в этом отдельном окне.

set "PROJECT=G:\Programming\Py\OSBB"
set "PYTHON=G:\Programming\Py\venv\Scripts\python.exe"
set "RUNNER=%PROJECT%\run_bot_guard_sandbox_v3.py"
set "SANDBOX=G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_live_services_2026-06-26_20-13-26.db"

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
    echo [ERROR] Не найдена clean sandbox:
    echo %SANDBOX%
    pause
    exit /b 1
)

echo Запускаю новую clean sandbox в отдельном окне.
echo Перед запуском остановите любой другой экземпляр Telegram-бота.
start "OSBB Live Service Sandbox" cmd.exe /k ""%PYTHON%" "%RUNNER%" --sandbox "%SANDBOX%" --run"

endlocal
