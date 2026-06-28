OSBB — service-code compatibility repair after phone-access V2
================================================================

Problem fixed
-------------
The two-barrier phone-access V2 package contained older SQL that requested:

    service_code

directly from service_items and payments. Your sandbox uses:

    base_service_code

Therefore opening "📞 Телефонный доступ" produced:

    no such column: service_code

What this repair changes
------------------------
Only three source files:

1. service_orders_core.py
2. service_preorders_core.py
3. Bots\handlers\service_orders_workspace.py

The new code reads either schema safely:

    service_code
or:
    base_service_code

It also restores safe automatic payment-to-order linking for payment rows that
have only the broad/base service code.

What this repair does NOT change
--------------------------------
- no SQLite data is changed;
- no payment is repeated;
- no notification is recreated;
- no subscription is created by the installer itself;
- no real barrier command is sent.

Your existing records remain the ones to continue:

    SI-20260627-000003
    N-20260627195153-000004
    receipt R2-20260627-000004
    payment #96

Installation
------------
1. Stop the sandbox bot with Ctrl+C.

2. Unpack this archive directly into:

    G:\Programming\Py\OSBB\

3. Run:

    RUN_INSTALL_service_code_compatibility_phone_v2.bat

4. Run:

    RUN_CHECK_service_code_compatibility_phone_v2.bat

Expected final line:

    CHECK PASSED

5. Start the normal sandbox bot:

    Start_OSBB_Live_Services_Sandbox_Bot_v1.bat

6. In Telegram open only:

    Главное меню → Админ-режим → 📞 Телефонный доступ

The existing confirmed payment should then be reconciled automatically and the
structured order should become visible. Do not create another cash notification
or another payment.

7. Open "📋 Оплаченные заявки" and send the order card before activation.

Source backups
--------------
The installer creates copies in:

    G:\Programming\Py\OSBB\Data\backups\source_code\
