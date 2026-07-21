@echo off
chcp 65001 >nul
title OSBB SANDBOX BOT (core_new)

echo ============================================================
echo    🏗️  OSBB SANDBOX BOT
echo    Новая архитектура core_new
echo    Версия: 0.1.0
echo    Дата: 2026-07-13
echo ============================================================
echo.
echo 📌 ВНИМАНИЕ: Это ПЕСОЧНИЦА!
echo    - Не влияет на основного бота
echo    - Работает с тестовой БД
echo    - Только для тестирования
echo.
echo 🔄 Активирую виртуальное окружение...
echo.

cd /d G:\Programming\Py
call venv\Scripts\activate.bat

echo ✅ Виртуальное окружение активировано
echo 🐍 Python: 
python --version
echo.
echo 🚀 Запускаю бота-песочницу...
echo.

python OSBB\Bots\sandbox_bot.py

echo.
echo ============================================================
echo ⚠️  Бот остановлен
echo ============================================================
pause