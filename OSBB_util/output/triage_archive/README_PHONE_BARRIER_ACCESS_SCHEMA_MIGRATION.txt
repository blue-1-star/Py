OSBB — миграция схемы телефонного доступа к двум шлагбаумам
================================================================

Цель
----
Этот комплект создаёт только новые таблицы и начальные настройки в специальной
live-services sandbox базе:

    G:\Programming\Py\OSBB\Data\db\sandbox\
    osbb_test_live_services_2026-06-26_20-13-26.db

Основная рабочая база osbb.db не открывается и не изменяется.

Что будет создано
-----------------
1. Два объекта доступа:
   BARRIER_FAR_01  — Далекий шлагбаум №1
   BARRIER_NEAR_02 — Ближній шлагбаум №2

2. Версионные тарифы:
   PHONE_BARRIER_ACCESS_CONNECT = 200 UAH за один шлагбаум, разово
   PHONE_BARRIER_ACCESS_MONTHLY = 100 UAH за один шлагбаум, в месяц

3. Версионная политика:
   PHONE_ACCESS_DEBT_GRACE_DAYS = 10
   PHONE_ACCESS_MONTHLY_START_RULE = MIDPOINT_OF_CALENDAR_MONTH
   PHONE_ACCESS_AUTO_DEACTIVATE_ENABLED = 1
   PHONE_ACCESS_DEFAULT_PARKING_DEBT_MODE = MANUAL_REVIEW
   PHONE_ACCESS_REAPPLICATION_NEW_SUBSCRIPTION = 1

4. Новые таблицы:
   access_points
   access_tariff_versions
   access_policy_versions
   access_policy_values
   phone_access_subscriptions
   phone_access_subscription_points
   phone_access_subscription_charges
   access_debt_warnings
   access_external_commands
   access_operation_journal
   access_schema_migrations

Что НЕ происходит
-----------------
- бот не меняется;
- существующие телефонные тесты, новые пульты, платежи и заявки не меняются;
- не создаются реальные абонплатные начисления;
- не создаются предупреждения;
- ничего не отключается;
- внешние команды настоящим шлагбаумам не отправляются.

Установка и запуск
------------------
1. Остановите live-services sandbox bot: Ctrl+C.

2. Распакуйте этот архив прямо в:

    G:\Programming\Py\OSBB\

   В корне OSBB должны появиться файлы:

    phone_barrier_access_core.py
    MIGRATE_phone_barrier_access_sandbox.py
    RUN_MIGRATE_phone_barrier_access_sandbox.bat
    CHECK_phone_barrier_access_sandbox_schema.py
    RUN_CHECK_phone_barrier_access_sandbox_schema.bat

3. Запустите:

    RUN_MIGRATE_phone_barrier_access_sandbox.bat

4. После сообщения MIGRATION COMPLETED запустите:

    RUN_CHECK_phone_barrier_access_sandbox_schema.bat

Ожидаемый результат проверки:
-----------------------------
- оба шлагбаума перечислены;
- разовое подключение = 200 UAH;
- абонплата = 100 UAH;
- льготный срок = 10 дней;
- правила первой абонплаты = MIDPOINT_OF_CALENDAR_MONTH;
- количество подписок и предупреждений = 0.

Безопасность
------------
Перед миграцией автоматически создаётся резервная копия sandbox DB в:

    G:\Programming\Py\OSBB\Data\db\sandbox\backups\

Миграция проверяет точный путь базы и не запускается на osbb.db.
