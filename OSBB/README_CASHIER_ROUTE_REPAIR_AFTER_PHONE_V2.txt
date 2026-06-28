OSBB — repair of the cashier route after phone-access V2
===========================================================

Why this repair is needed
-------------------------
If pressing "💰 Касса" returns a generic message:

    Вы нажали: 💰 Касса

then the client-portal fallback has intercepted the button before cashier v2.
The pending cash notification was NOT confirmed and no payment/order data was
changed.

This repair restores the sandbox launcher that dynamically places cashier v2
before the client portal every time the bot starts.

What this repair changes
------------------------
Only one source file is replaced:

    G:\Programming\Py\OSBB\run_bot_live_services_sandbox_v1.py

A backup is made first in:

    G:\Programming\Py\OSBB\Data\backups\source_code\

No database, service order, payment notification, phone-access subscription,
or Bot source file is changed.

Installation
------------
1. Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat with Ctrl+C.

2. Unpack this archive into:

    G:\Programming\Py\OSBB\

3. Run:

    RUN_INSTALL_cashier_route_after_phone_v2.bat

4. Run the non-polling check:

    RUN_CHECK_cashier_route_after_phone_v2.bat

The check must show under Runtime changes either:

    cashier route: placed before client portal

or:

    cashier route: already before client portal

and finish with:

    CHECK PASSED

5. Start the normal bot:

    Start_OSBB_Live_Services_Sandbox_Bot_v1.bat

6. In Telegram retry:

    Главне меню → Адмін-режим → 💰 Каса

It must open the cashier menu, not the generic "Вы нажали" response.

Then confirm the already-created notification only:

    N-20260627195153-000004
    SI-20260627-000003
    400 UAH

Do not create a second notification.
