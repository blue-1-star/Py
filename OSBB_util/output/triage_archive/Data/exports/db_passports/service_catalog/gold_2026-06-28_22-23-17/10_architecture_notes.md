# Architecture notes for service_catalog

## Автоматическое архитектурное заключение

`service_catalog` выглядит как центральный справочник услуг OSBB.
Он уже содержит признаки, которые подходят для политики доступа: `is_access_control`, `is_cash_collectable`, `is_monthly`, `is_fundraising`, `is_commercial`.

Потенциальные расширения для политики задолженности, которых сейчас нет:
- `requires_no_debt`
- `block_order`
- `block_issue`
- `block_activation`
- `manual_review`
- `debt_message`

Рекомендация v1: не создавать отдельный справочник услуг. Расширять политику поверх существующих `service_code`.

Наиболее упоминаемые service_code:
- `COMMERCIAL_CONTRACT`: refs=249, rows=1
- `PARKING_DAY`: refs=65, rows=1
- `IMPROVEMENT`: refs=61, rows=1
- `PARKING_NIGHT`: refs=60, rows=1
- `BARRIER_PHONE`: refs=46, rows=1
- `BARRIER_PHONE_CONNECT`: refs=15, rows=1
- `BARRIER_REPAIR`: refs=14, rows=1
- `PARKING_EQUIPMENT`: refs=6, rows=1
- `GUEST_PARKING`: refs=5, rows=1
- `HISTORICAL_UNCLASSIFIED`: refs=4, rows=1

Найдено ссылок в коде всего: 1900
Из них потенциальных write/schema контекстов: 83
