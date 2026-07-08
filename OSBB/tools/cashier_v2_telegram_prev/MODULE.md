# Cashier v2 Telegram Adapter v0.1

This module does not create a new payment system.

It connects Telegram to existing root-level:

```text
cashier_v2_core.py
```

## Features

- cashier v2 schema status;
- reconciliation summary;
- last cashier receipts;
- open resident payment notices;
- confirm cash resident notice;
- create cash receipt + payment through `cashier_v2_core.create_cash_receipt()`.

## Telegram flow

```text
💳 Платежи
    📊 Сводка кассы
    ➕ Принять наличные
    📨 Уведомления жителей
    📜 Последние чеки
```

## Manual cash flow

```text
Квартира
Сумма
Период
Услуга
Основание
Подтверждение
```

## Important

This adapter requires the existing cashier v2 DB schema to be ready.
It calls `cashier_v2_core.schema_ready()`.
