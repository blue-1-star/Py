ОСББ — live-services sandbox bundle
===================================

Назначение
----------
Этот набор возвращает вас к фактической заявке:
SO-20260626-000001, кв. 174, «ТЕСТ — перепрошивка собственного пульта».

Рабочая база этого теста:
Data\db\sandbox\osbb_test_live_services_2026-06-26_20-13-26.db

Что исправлено
-------------
1. Новый runtime-маршрут подключает service_orders_workspace к существующему
   parking_bot.py без постоянного изменения parking_bot.py.
2. service_orders_workspace работает со старой таблицей payments:
   - отсутствует source_ref;
   - вместо apartment_id есть apartment_number.
3. Launcher создаёт только в sandbox отдельные права тестового оператора.
   Перед этим он делает копию sandbox-БД в Data\db\sandbox\backups.
4. Старый guard-sandbox не используется.

Установка
----------
1. Распакуйте СОДЕРЖИМОЕ этого ZIP прямо в:
   G:\Programming\Py\OSBB\
   Подтвердите замену одного файла:
   Bots\handlers\service_orders_workspace.py

2. Если всё ещё открыты окна Start_OSBB_Guard_Sandbox_Bot_v2.bat,
   сначала запустите:
   STOP_old_guard_sandbox_bots.bat

3. Запустите:
   Start_OSBB_Live_Services_Sandbox_Bot_v1.bat

Terminal will show the number of matching confirmed payments for the open order.

Telegram path
-------------
After launch:
  /start
  choose language
  Админ-режим
  🔑 Заявки на пульты
  📋 Открытые заявки
  open SO-20260626-000001

Expected step sequence:
  ✅ Пульт жильца принят
  → 💳 Привязать оплату
  → 🛠 Перепрошивка выполнена
  → 📤 Вернуть пульт жильцу

No matching payment
-------------------
If the launcher prints:
  matching confirmed payments for this order: 0

close the live-services bot with Ctrl+C, run:
  CREATE_TEST_PAYMENT_FOR_OPEN_SERVICE_ORDER.bat

This makes one expressly labelled TEST payment only in the live-services sandbox
and automatically backs up that sandbox first. Restart the live-services bot,
then choose 💳 Привязать оплату.

Do not use Start_OSBB_Guard_Sandbox_Bot_v2.bat for this order.
