# Service Orders UI v2 patch report

Generated: `2026-07-04 16:58:31`
Dry run: `True`
Bot: `G:\Programming\Py\OSBB\Bots\parking_bot.py`

## Changes

- service workspace import
- client_portal_v3 import
- mode menu service operator button
- service active route after lang/t
- service general route
- service operator mode switch

## Preview

`G:\Programming\Py\OSBB\Recovered\parking_bot_service_orders_ui_v2_2026-07-04_16-58-31.patched.py`

## Diff

`G:\Programming\Py\OSBB\Recovered\parking_bot_service_orders_ui_v2_2026-07-04_16-58-31.diff`

## Required markers

- OK `from handlers.service_orders_workspace import (`
- OK `from handlers.client_portal_v3 import (`
- OK `handle_service_orders_text(`
- OK `show_service_operator_workspace(`
- OK `🔑 Оператор услуг`
- OK `Заказы услуг: житель и оператор`
- OK `Операторский кабинет услуг`

## Safety check

- `t = TEXTS[lang]` position: `25063`
- service active block position: `25120`
- service block after t: `True`

