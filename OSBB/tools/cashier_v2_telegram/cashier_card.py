#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any


def period_display(period: str | None) -> str:
    if not period:
        return '—'
    parts = str(period).split('-')
    if len(parts) == 2 and len(parts[0]) == 4:
        return f"{parts[1]}-{parts[0]}"
    return str(period)


def money(value: Any) -> str:
    if value is None or value == '':
        return 'не определена'
    try:
        amount = float(value)
    except Exception:
        return 'не определена'
    return f"{amount:.2f}"


def payer_title(payer: dict) -> str:
    if payer.get('kind') == 'vehicle':
        return f"🚗 {payer.get('plate') or '—'}"
    if payer.get('kind') == 'commercial':
        return f"🏢 {payer.get('counterparty_name') or 'Без названия'}"
    return f"🏠 Квартира {payer.get('apartment_number') or '—'}"


def payment_card(draft: dict) -> str:
    payer = draft.get('payer') or {}
    service = draft.get('service') or {}
    vehicle = payer.get('vehicle') or {}
    parking = payer.get('parking_time') or vehicle.get('parking_time') or draft.get('service_group') or '—'
    service_name = service.get('service_name') or service.get('service_item_name') or service.get('service_code') or '—'
    comment = draft.get('comment') or '—'

    lines = [
        payer_title(payer),
        '',
        f"Квартира: {payer.get('apartment_number') or '—'}",
    ]
    if payer.get('kind') == 'vehicle':
        lines.extend([
            f"Режим парковки: {parking}",
            f"Модель: {vehicle.get('car_model') or '—'}",
        ])
    elif payer.get('kind') == 'commercial':
        lines.extend([
            f"Код помещения: {payer.get('unit_code') or payer.get('apartment_number') or '—'}",
            f"Договор: {payer.get('contract_number') or 'черновик / без номера'}",
            f"Статус договора: {payer.get('contract_status') or 'не создан'}",
            f"Условие: {payer.get('item_names') or 'не заполнено'}",
        ])
    lines.extend([
        '',
        f"Услуга: {service_name}",
        f"Последний оплаченный период: {period_display(draft.get('latest_paid_period'))}",
        f"Предлагаемый период: {period_display(draft.get('period_code'))}",
        f"Сумма: {money(draft.get('amount'))} UAH",
        f"Комментарий: {comment}",
        '',
        'Если всё верно — подтвердите. Иначе измените только нужное поле.',
    ])
    return '\n'.join(lines)


def success_card(result: dict, draft: dict) -> str:
    payer = draft.get('payer') or {}
    return '\n'.join([
        '✅ Оплата принята',
        '',
        payer_title(payer),
        f"Квартира: {payer.get('apartment_number') or '—'}",
        f"Период: {period_display(draft.get('period_code'))}",
        f"Сумма: {money(draft.get('amount'))} UAH",
        f"Чек: {result.get('receipt_number') or '—'}",
        f"Payment ID: {result.get('payment_id') or '—'}",
    ])
