#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram adapter for existing OSBB Cashier v2 core.

This module does not create a second cashier system.
It calls existing root-level cashier_v2_core.py functions:
- schema_ready()
- reconciliation_summary()
- resolve_physical_unit()
- service_options()
- create_cash_receipt()
- list_open_notices()
- confirm_cash_notice()
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Any

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cashier_v2_core as core  # existing OSBB cashier core


BTN_PAYMENTS = "💳 Платежи"
BTN_CASHIER_V2 = "💰 Касса v2"
BTN_SUMMARY = "📊 Сводка кассы"
BTN_NEW_CASH = "➕ Принять наличные"
BTN_OPEN_NOTICES = "📨 Уведомления жителей"
BTN_LAST_RECEIPTS = "📜 Последние чеки"
BTN_CONFIRM = "✅ Подтвердить"
BTN_CANCEL = "❌ Отмена"
BTN_BACK = "⬅ Назад"
BTN_MAIN_MENU = "🏠 Главное меню"

DEFAULT_CASHBOX_CODE = "O"
MAX_SERVICE_BUTTONS = 12


def kb(rows: list[list[str]]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def menu_kb() -> ReplyKeyboardMarkup:
    return kb([
        [BTN_SUMMARY],
        [BTN_NEW_CASH],
        [BTN_OPEN_NOTICES, BTN_LAST_RECEIPTS],
        [BTN_BACK, BTN_MAIN_MENU],
    ])


def back_kb() -> ReplyKeyboardMarkup:
    return kb([[BTN_CANCEL], [BTN_BACK, BTN_MAIN_MENU]])


def confirm_kb() -> ReplyKeyboardMarkup:
    return kb([[BTN_CONFIRM], [BTN_CANCEL]])


def service_kb(options: list[dict]) -> ReplyKeyboardMarkup:
    rows: list[list[str]] = []
    for idx, opt in enumerate(options[:MAX_SERVICE_BUTTONS], 1):
        label = core.service_label(opt)
        if len(label) > 45:
            label = label[:42] + "..."
        rows.append([f"{idx}. {label}"])
    rows.append([BTN_CANCEL])
    return kb(rows)


def notice_kb(rows: list[dict]) -> ReplyKeyboardMarkup:
    buttons: list[list[str]] = []
    for row in rows[:10]:
        buttons.append([f"✅ Уведомление #{row['id']} {row.get('notice_number') or ''}".strip()])
    buttons.append([BTN_BACK])
    return kb(buttons)


def money(value: Any) -> str:
    try:
        return f"{float(value):.2f}"
    except Exception:
        return "0.00"


def parse_amount(text: str) -> float | None:
    try:
        amount = float(text.strip().replace(",", "."))
    except ValueError:
        return None
    return amount if amount > 0 else None


def schema_status_text() -> str:
    ok, msg = core.schema_ready()
    if ok:
        return "✅ Касса v2 готова."
    return "⚠ Касса v2 не готова:\n" + msg


def summary_text() -> str:
    ok, msg = core.schema_ready()
    if not ok:
        return "⚠ Касса v2 не готова:\n" + msg

    data = core.reconciliation_summary()
    return (
        "📊 Сводка кассы v2\n\n"
        f"Уведомления жителей: {data.get('resident_notices', 0)}\n"
        f"Бумажные заметки: {data.get('paper_notes', 0)}\n"
        f"Неразнесённая наличка: {data.get('unallocated_cash', 0)}\n"
        f"Исторические импорты: {data.get('historical_imports', 0)}\n"
        f"Открытые сверки: {data.get('open_cases', 0)}"
    )


def last_receipts(limit: int = 7) -> list[sqlite3.Row]:
    conn = core.get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM cashier_receipts
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return cur.fetchall()
    finally:
        conn.close()


def format_receipt(row: sqlite3.Row, n: int) -> str:
    return (
        f"{n}. Чек #{row['id']} / {row['receipt_number']}\n"
        f"Квартира: {row['apartment_number'] or '—'}\n"
        f"Дата: {row['receipt_date'] or '—'}\n"
        f"Касса: {row['cashbox_code'] or '—'}\n"
        f"Сумма: {money(row['amount'])} {row['currency'] or 'UAH'}\n"
        f"Статус: {row['entry_status'] or '—'}\n"
        f"Услуга: {row['service_item_code'] or row['service_hint'] or '—'}"
    )


def last_receipts_text() -> str:
    rows = last_receipts()
    if not rows:
        return "📜 Последние чеки\n\nЗаписей нет."
    parts = ["📜 Последние чеки", ""]
    for i, row in enumerate(rows, 1):
        parts.append(format_receipt(row, i))
        parts.append("────────────────")
    return "\n".join(parts).rstrip("─\n")


def open_notices() -> list[dict]:
    return core.list_open_notices(10)


def open_notices_text(rows: list[dict]) -> str:
    if not rows:
        return "📨 Уведомления жителей\n\nНовых уведомлений нет."
    parts = ["📨 Уведомления жителей", ""]
    for i, row in enumerate(rows, 1):
        parts.append(
            f"{i}. Уведомление #{row['id']} / {row.get('notice_number') or '—'}\n"
            f"Квартира: {row.get('apartment_number') or '—'}\n"
            f"Тип: {row.get('notice_type') or '—'}\n"
            f"Касса: {row.get('declared_cashbox_code') or '—'}\n"
            f"Период: {row.get('declared_period_code') or '—'}\n"
            f"Сумма: {money(row.get('declared_amount'))} UAH\n"
            f"Услуга: {row.get('declared_service_item_code') or row.get('declared_service_code') or '—'}"
        )
        parts.append("────────────────")
    return "\n".join(parts).rstrip("─\n")


def draft_text(d: dict[str, Any]) -> str:
    apartment = d.get("apartment") or {}
    service = d.get("service") or {}
    return (
        "💰 Принять наличные\n\n"
        f"Квартира: {apartment.get('apartment_number') or '—'}\n"
        f"Сумма: {money(d.get('amount'))} UAH\n"
        f"Период: {d.get('period_code') or '—'}\n"
        f"Касса: {d.get('cashbox_code') or DEFAULT_CASHBOX_CODE}\n"
        f"Услуга: {core.service_label(service) if service else '—'}\n"
        f"Основание: {d.get('source_text') or '—'}\n\n"
        "Сохранить чек и оплату через cashier_v2_core?"
    )


async def show_cashier_v2(update: Update, user_states: dict[int, Any], user_id: int) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "menu"}
    await update.message.reply_text(
        "💰 Касса v2\n\n"
        + schema_status_text()
        + "\n\nРаботаем через существующее ядро cashier_v2_core.py.",
        reply_markup=menu_kb(),
    )


async def start_new_cash(update: Update, user_states: dict[int, Any], user_id: int) -> None:
    user_states[user_id] = {
        "mode": "cashier_v2",
        "screen": "new_cash_apartment",
        "draft": {"cashbox_code": DEFAULT_CASHBOX_CODE},
    }
    await update.message.reply_text(
        "➕ Принять наличные\n\nВведите номер квартиры:",
        reply_markup=back_kb(),
    )


async def handle_cashier_v2_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_states: dict[int, Any],
    user_id: int,
) -> bool:
    text = (update.message.text or "").strip()
    state = user_states.get(user_id, {})

    if state.get("mode") != "cashier_v2" and text not in {BTN_PAYMENTS, BTN_CASHIER_V2}:
        return False

    if text in {BTN_PAYMENTS, BTN_CASHIER_V2}:
        await show_cashier_v2(update, user_states, user_id)
        return True

    if text == BTN_MAIN_MENU:
        user_states[user_id] = {}
        await update.message.reply_text("🏠 Главное меню")
        return True

    if text in {BTN_BACK, BTN_CANCEL}:
        await show_cashier_v2(update, user_states, user_id)
        return True

    if text == BTN_SUMMARY:
        await update.message.reply_text(summary_text(), reply_markup=menu_kb())
        return True

    if text == BTN_LAST_RECEIPTS:
        await update.message.reply_text(last_receipts_text(), reply_markup=menu_kb())
        return True

    if text == BTN_OPEN_NOTICES:
        rows = open_notices()
        user_states[user_id] = {
            "mode": "cashier_v2",
            "screen": "open_notices",
            "notice_ids": [int(r["id"]) for r in rows],
        }
        await update.message.reply_text(open_notices_text(rows), reply_markup=notice_kb(rows))
        return True

    if text == BTN_NEW_CASH:
        await start_new_cash(update, user_states, user_id)
        return True

    if state.get("screen") == "open_notices":
        if text.startswith("✅ Уведомление #"):
            try:
                notice_id = int(text.split("#", 1)[1].split()[0])
            except Exception:
                await update.message.reply_text("⚠ Не понял номер уведомления.", reply_markup=menu_kb())
                return True
            try:
                result = core.confirm_cash_notice(
                    notice_id,
                    operator_id=int(user_id),
                    operator_note="Подтверждено через Telegram касса v2",
                )
                await update.message.reply_text(
                    "✅ Уведомление подтверждено.\n"
                    f"Чек: {result.get('receipt_number')}\n"
                    f"Payment ID: {result.get('payment_id')}",
                    reply_markup=menu_kb(),
                )
            except Exception as e:
                await update.message.reply_text("⚠ Ошибка подтверждения:\n" + str(e), reply_markup=menu_kb())
            return True

    if state.get("screen") == "new_cash_apartment":
        kind, units, message = core.resolve_physical_unit(text)
        if kind != "UNIT" or not units:
            await update.message.reply_text(
                "⚠ Квартира не выбрана.\n"
                + (message or "Введите точный номер физической квартиры."),
                reply_markup=back_kb(),
            )
            return True
        draft = state.get("draft") or {}
        draft["apartment"] = units[0]
        user_states[user_id] = {"mode": "cashier_v2", "screen": "new_cash_amount", "draft": draft}
        await update.message.reply_text(
            f"Квартира: {units[0].get('apartment_number')}\n\nВведите сумму:",
            reply_markup=back_kb(),
        )
        return True

    if state.get("screen") == "new_cash_amount":
        amount = parse_amount(text)
        if amount is None:
            await update.message.reply_text("⚠ Введите сумму числом, например 400 или 400,50.", reply_markup=back_kb())
            return True
        draft = state.get("draft") or {}
        draft["amount"] = amount
        user_states[user_id] = {"mode": "cashier_v2", "screen": "new_cash_period", "draft": draft}
        await update.message.reply_text(
            "Введите период, например 2026-06 или 05-06_26.\n"
            "Для пропуска отправьте «-».",
            reply_markup=back_kb(),
        )
        return True

    if state.get("screen") == "new_cash_period":
        draft = state.get("draft") or {}
        period = None if text in {"-", "—"} else core.normalize_period(text)
        draft["period_code"] = period
        options = core.service_options(period)
        if not options:
            await update.message.reply_text("⚠ В справочнике услуг нет доступных услуг.", reply_markup=menu_kb())
            await show_cashier_v2(update, user_states, user_id)
            return True
        user_states[user_id] = {
            "mode": "cashier_v2",
            "screen": "new_cash_service",
            "draft": draft,
            "service_options": options[:MAX_SERVICE_BUTTONS],
        }
        await update.message.reply_text("Выберите услугу:", reply_markup=service_kb(options))
        return True

    if state.get("screen") == "new_cash_service":
        try:
            idx = int(text.split(".", 1)[0]) - 1
        except Exception:
            await update.message.reply_text("⚠ Выберите услугу кнопкой.", reply_markup=service_kb(state.get("service_options") or []))
            return True
        options = state.get("service_options") or []
        if idx < 0 or idx >= len(options):
            await update.message.reply_text("⚠ Такой услуги нет в списке.", reply_markup=service_kb(options))
            return True
        draft = state.get("draft") or {}
        draft["service"] = options[idx]
        user_states[user_id] = {"mode": "cashier_v2", "screen": "new_cash_source", "draft": draft}
        await update.message.reply_text(
            "Введите основание/комментарий.\n"
            "Например: бумажка консьержа, лист 3, строка 12",
            reply_markup=back_kb(),
        )
        return True

    if state.get("screen") == "new_cash_source":
        if not text or text in {"-", "—"}:
            await update.message.reply_text("⚠ Основание обязательно для cash receipt.", reply_markup=back_kb())
            return True
        draft = state.get("draft") or {}
        draft["source_text"] = text
        user_states[user_id] = {"mode": "cashier_v2", "screen": "new_cash_confirm", "draft": draft}
        await update.message.reply_text(draft_text(draft), reply_markup=confirm_kb())
        return True

    if state.get("screen") == "new_cash_confirm":
        if text != BTN_CONFIRM:
            await update.message.reply_text("Нажмите «Подтвердить» или «Отмена».", reply_markup=confirm_kb())
            return True

        draft = state.get("draft") or {}
        conn = core.get_conn()
        try:
            cur = conn.cursor()
            result = core.create_cash_receipt(
                cur,
                apartment=draft["apartment"],
                cashbox_code=draft.get("cashbox_code") or DEFAULT_CASHBOX_CODE,
                receipt_date=core.today(),
                period_code=draft.get("period_code"),
                service=draft["service"],
                amount=float(draft["amount"]),
                source_text=draft["source_text"],
                operator_id=int(user_id),
                origin_kind="HAND_TO_HAND",
            )
            conn.commit()
            await update.message.reply_text(
                "✅ Оплата принята через cashier_v2_core.py\n\n"
                f"Чек: {result.get('receipt_number')}\n"
                f"Receipt ID: {result.get('receipt_id')}\n"
                f"Payment ID: {result.get('payment_id')}",
                reply_markup=menu_kb(),
            )
            user_states[user_id] = {"mode": "cashier_v2", "screen": "menu"}
        except Exception as e:
            conn.rollback()
            await update.message.reply_text("⚠ Ошибка сохранения:\n" + str(e), reply_markup=menu_kb())
        finally:
            conn.close()
        return True

    return False
