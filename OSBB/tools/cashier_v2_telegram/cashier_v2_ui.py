#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram adapter for existing OSBB Cashier v2 core.

v0.2:
- main cash flow: Night / Day / Misc, not raw service dump;
- period selection by buttons;
- payer search by apartment number or vehicle plate;
- Misc service groups;
- TEST services hidden from normal flow.
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import date
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
BTN_CASH = "💵 Наличные"
BTN_OPEN_NOTICES = "📨 Уведомления жителей"
BTN_LAST_RECEIPTS = "📜 Последние чеки"

BTN_NIGHT = "🌙 Night"
BTN_DAY = "☀️ Day"
BTN_MISC = "📦 Другое"

BTN_CUSTOM_PERIOD = "📅 Другой период"
BTN_NO_PERIOD = "❔ Без периода"

BTN_BATCH_ENTRANCE = "⚡ Пачка подъезда"
BTN_ACTUAL_FEE = "📌 Актуальный сбор"
BTN_REMOTES = "🔑 Пульты"
BTN_PHONE = "📞 Телефонный доступ"
BTN_COMMON_FEES = "🧰 Общие сборы"
BTN_PARKING_PLACES = "🅿️ Паркоместа"
BTN_COMMERCIAL = "🏢 Коммерческие"
BTN_TEST_SERVICES = "🧪 Тестовые услуги"

BTN_CONFIRM = "✅ Подтвердить"
BTN_CANCEL = "❌ Отмена"
BTN_BACK = "⬅️ К кассе"
BTN_MAIN_MENU = "🏠 Главное меню"

DEFAULT_CASHBOX_CODE = "O"
MAX_SERVICE_BUTTONS = 12


def kb(rows: list[list[str]]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def menu_kb() -> ReplyKeyboardMarkup:
    return kb([
        [BTN_CASH],
        [BTN_BATCH_ENTRANCE],
        [BTN_OPEN_NOTICES, BTN_LAST_RECEIPTS],
        [BTN_SUMMARY],
        [BTN_BACK, BTN_MAIN_MENU],
    ])


def cash_type_kb() -> ReplyKeyboardMarkup:
    return kb([
        [BTN_NIGHT, BTN_DAY],
        [BTN_MISC],
        [BTN_BACK, BTN_MAIN_MENU],
    ])


def misc_group_kb() -> ReplyKeyboardMarkup:
    return kb([
        [BTN_ACTUAL_FEE],
        [BTN_REMOTES, BTN_PHONE],
        [BTN_COMMON_FEES],
        [BTN_PARKING_PLACES],
        [BTN_COMMERCIAL],
        [BTN_TEST_SERVICES],
        [BTN_BACK, BTN_MAIN_MENU],
    ])


def period_kb() -> ReplyKeyboardMarkup:
    p = suggested_periods()
    return kb([
        [p[0], p[1]],
        [p[2], p[3]],
        [BTN_CUSTOM_PERIOD, BTN_NO_PERIOD],
        [BTN_BACK, BTN_MAIN_MENU],
    ])


def back_kb() -> ReplyKeyboardMarkup:
    return kb([[BTN_BACK, BTN_MAIN_MENU]])


def confirm_kb() -> ReplyKeyboardMarkup:
    return kb([[BTN_CONFIRM], [BTN_CANCEL]])


def service_kb(options: list[dict]) -> ReplyKeyboardMarkup:
    rows: list[list[str]] = []
    for idx, opt in enumerate(options[:MAX_SERVICE_BUTTONS], 1):
        label = service_label_clean(opt)
        if len(label) > 56:
            label = label[:53] + "..."
        rows.append([f"{idx}. {label}"])
    rows.append([BTN_BACK, BTN_MAIN_MENU])
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


def month_add(year: int, month: int, delta: int) -> tuple[int, int]:
    m = month + delta
    y = year
    while m <= 0:
        y -= 1
        m += 12
    while m > 12:
        y += 1
        m -= 12
    return y, m


def period_code(y: int, m: int) -> str:
    return f"{y:04d}-{m:02d}"


def default_period() -> str:
    today = date.today()
    # до 15 числа включительно — текущий месяц, после 15-го — следующий
    delta = 0 if today.day <= 15 else 1
    y, m = month_add(today.year, today.month, delta)
    return period_code(y, m)


def suggested_periods() -> list[str]:
    y, m = map(int, default_period().split("-"))
    return [period_code(*month_add(y, m, delta)) for delta in (-2, -1, 0, 1)]


def option_text(opt: dict) -> str:
    keys = (
        "service_item_code", "base_service_code", "service_code", "service_type",
        "display_name", "service_name", "name", "label", "title",
        "public_name_uk", "public_name_ru", "description",
    )
    return " ".join(str(opt.get(k) or "") for k in keys).lower()


def service_label_clean(opt: dict) -> str:
    label = core.service_label(opt)
    return label.replace("ТЕСТ — ", "").replace("TEST — ", "").strip()


def is_test_service(opt: dict) -> bool:
    t = option_text(opt)
    return "test" in t or "тест" in t


def all_services(period: str | None) -> list[dict]:
    try:
        return list(core.service_options(period))
    except Exception:
        return []


def filter_services(period: str | None, group: str) -> list[dict]:
    options = all_services(period)
    out: list[dict] = []

    for opt in options:
        t = option_text(opt)

        if group != "test" and is_test_service(opt):
            continue

        if group == "night":
            ok = "night" in t or "ноч" in t
        elif group == "day":
            ok = "day" in t or "днев" in t or "день" in t
        elif group == "remote":
            ok = "пульт" in t or "remote" in t
        elif group == "phone":
            ok = "телефон" in t or "phone" in t or "access" in t
        elif group == "common":
            ok = "благо" in t or "ремонт" in t or "оборуд" in t or "збір" in t or "сбор" in t
        elif group == "parking_place":
            ok = "паркомест" in t or "гост" in t or "аренд" in t or "оренд" in t or "продаж" in t
        elif group == "commercial":
            ok = "commercial" in t or "коммер" in t or "фирм" in t or "догов" in t or "contract" in t
        elif group == "actual":
            ok = "актуаль" in t or "парков" in t or "parking" in t
        elif group == "test":
            ok = is_test_service(opt)
        else:
            ok = True

        if ok:
            out.append(opt)

    return out


def find_payers(query: str) -> list[dict]:
    q = query.strip()
    results: list[dict] = []

    # Apartment search through existing core resolver.
    try:
        kind, units, message = core.resolve_physical_unit(q)
        if kind == "UNIT" and units:
            for u in units[:8]:
                ap = str(u.get("apartment_number") or q)
                results.append({
                    "kind": "apartment",
                    "apartment_number": ap,
                    "apartment": u,
                    "label": f"🏠 квартира {ap}",
                })
        elif units:
            for u in units[:8]:
                ap = str(u.get("apartment_number") or "")
                results.append({
                    "kind": "apartment",
                    "apartment_number": ap,
                    "apartment": u,
                    "label": f"🏠 квартира {ap}",
                })
    except Exception:
        pass

    # Vehicle plate search.
    conn = core.get_conn()
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if cur.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='vehicles'").fetchone():
            like = "%" + q.replace(" ", "").upper() + "%"
            rows = cur.execute(
                """
                SELECT v.*, a.apartment_number
                FROM vehicles v
                LEFT JOIN apartments a ON a.id=v.apartment_id
                WHERE UPPER(REPLACE(COALESCE(v.license_plate,''),' ','')) LIKE ?
                   OR UPPER(REPLACE(COALESCE(v.license_plate_normalized,''),' ','')) LIKE ?
                ORDER BY a.apartment_number, v.license_plate
                LIMIT 8
                """,
                (like, like),
            ).fetchall()
            for r in rows:
                ap = str(r["apartment_number"] or "")
                plate = r["license_plate"] or r["license_plate_normalized"] or q
                results.append({
                    "kind": "vehicle",
                    "apartment_number": ap,
                    "vehicle_id": r["id"],
                    "plate": plate,
                    "parking_time": r["parking_time"] if "parking_time" in r.keys() else None,
                    "label": f"🚗 {plate} / кв. {ap}",
                })
    except Exception:
        pass
    finally:
        conn.close()

    seen = set()
    unique = []
    for item in results:
        key = item["label"]
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique[:10]


def payer_kb(items: list[dict]) -> ReplyKeyboardMarkup:
    rows = [[f"{i+1}. {item['label']}"] for i, item in enumerate(items)]
    rows.append([BTN_BACK, BTN_MAIN_MENU])
    return kb(rows)


def payer_to_apartment(payer: dict) -> dict:
    if payer.get("apartment"):
        return payer["apartment"]
    return {"apartment_number": payer.get("apartment_number")}


def schema_status_text() -> str:
    ok, msg = core.schema_ready()
    return "✅ Касса v2 готова." if ok else "⚠ Касса v2 не готова:\n" + msg


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
        cur.execute("SELECT * FROM cashier_receipts ORDER BY id DESC LIMIT ?", (limit,))
        return cur.fetchall()
    finally:
        conn.close()


def last_receipts_text() -> str:
    rows = last_receipts()
    if not rows:
        return "📜 Последние чеки\n\nЗаписей нет."
    parts = ["📜 Последние чеки", ""]
    for i, row in enumerate(rows, 1):
        parts.append(
            f"{i}. Чек #{row['id']} / {row['receipt_number']}\n"
            f"Квартира: {row['apartment_number'] or '—'}\n"
            f"Дата: {row['receipt_date'] or '—'}\n"
            f"Касса: {row['cashbox_code'] or '—'}\n"
            f"Сумма: {money(row['amount'])} {row['currency'] or 'UAH'}\n"
            f"Статус: {row['entry_status'] or '—'}\n"
            f"Услуга: {row['service_item_code'] or row['service_hint'] or '—'}"
        )
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
            f"Период: {row.get('declared_period_code') or '—'}\n"
            f"Сумма: {money(row.get('declared_amount'))} UAH\n"
            f"Услуга: {row.get('declared_service_item_code') or row.get('declared_service_code') or '—'}"
        )
        parts.append("────────────────")
    return "\n".join(parts).rstrip("─\n")


def draft_text(d: dict[str, Any]) -> str:
    payer = d.get("payer") or {}
    service = d.get("service") or {}
    return (
        "💰 Принять наличные\n\n"
        f"Плательщик: {payer.get('label') or '—'}\n"
        f"Квартира: {payer.get('apartment_number') or '—'}\n"
        f"Сумма: {money(d.get('amount'))} UAH\n"
        f"Период: {d.get('period_code') or '—'}\n"
        f"Касса: {d.get('cashbox_code') or DEFAULT_CASHBOX_CODE}\n"
        f"Услуга: {service_label_clean(service) if service else '—'}\n"
        f"Основание: {d.get('source_text') or '—'}\n\n"
        "Сохранить чек и оплату через cashier_v2_core?"
    )


async def show_cashier_v2(update: Update, user_states: dict[int, Any], user_id: int) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "menu"}
    await update.message.reply_text(
        "💰 Касса и платежи v2\n\n"
        "O — основная касса охраны.\n"
        "K1–K6 — отдельные кассы консьержей.\n"
        "BANK — банковский канал, не физическая касса.\n\n"
        "Уведомление жителя само по себе не является оплатой.",
        reply_markup=menu_kb(),
    )


async def start_cash(update: Update, user_states: dict[int, Any], user_id: int) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "cash_type", "draft": {"cashbox_code": DEFAULT_CASHBOX_CODE}}
    await update.message.reply_text("💵 Наличные\n\nВыберите тип оплаты:", reply_markup=cash_type_kb())


async def ask_period(update: Update, user_states: dict[int, Any], user_id: int, draft: dict[str, Any]) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "period", "draft": draft}
    await update.message.reply_text(
        "Выберите период оплаты.\n"
        f"Период по умолчанию: {default_period()}",
        reply_markup=period_kb(),
    )


async def ask_payer(update: Update, user_states: dict[int, Any], user_id: int, draft: dict[str, Any]) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "payer_query", "draft": draft}
    await update.message.reply_text(
        "Введите номер квартиры или номер автомобиля.\n\n"
        "Если у квартиры несколько авто, дальше выберем нужное.",
        reply_markup=back_kb(),
    )


async def ask_amount(update: Update, user_states: dict[int, Any], user_id: int, draft: dict[str, Any]) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "amount", "draft": draft}
    await update.message.reply_text("Введите сумму оплаты:", reply_markup=back_kb())


async def ask_source(update: Update, user_states: dict[int, Any], user_id: int, draft: dict[str, Any]) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "source", "draft": draft}
    await update.message.reply_text("Введите основание/комментарий:", reply_markup=back_kb())


async def choose_service_group(update: Update, user_states: dict[int, Any], user_id: int, draft: dict[str, Any]) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "misc_group", "draft": draft}
    await update.message.reply_text("📦 Другое\n\nВыберите группу услуги:", reply_markup=misc_group_kb())


async def show_services(update: Update, user_states: dict[int, Any], user_id: int, draft: dict[str, Any], group: str) -> None:
    options = filter_services(draft.get("period_code"), group)
    if not options:
        await update.message.reply_text("⚠ Для этой группы услуги не найдены.", reply_markup=menu_kb())
        return
    user_states[user_id] = {"mode": "cashier_v2", "screen": "service", "draft": draft, "service_options": options[:MAX_SERVICE_BUTTONS]}
    await update.message.reply_text("Выберите услугу из справочника:", reply_markup=service_kb(options))


async def handle_cashier_v2_text(update: Update, context: ContextTypes.DEFAULT_TYPE, user_states: dict[int, Any], user_id: int) -> bool:
    text = (update.message.text or "").strip()
    state = user_states.get(user_id, {})

    if state.get("mode") != "cashier_v2" and text not in {BTN_PAYMENTS, BTN_CASHIER_V2, "💰 Касса"}:
        return False

    if text in {BTN_PAYMENTS, BTN_CASHIER_V2, "💰 Касса"}:
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
        user_states[user_id] = {"mode": "cashier_v2", "screen": "open_notices"}
        await update.message.reply_text(open_notices_text(rows), reply_markup=notice_kb(rows))
        return True

    if text == BTN_CASH:
        await start_cash(update, user_states, user_id)
        return True

    if text == BTN_BATCH_ENTRANCE:
        await update.message.reply_text(
            "⚡ Массовый ввод по подъезду\n\n"
            "В v0.2 отключён для реальных оплат. Переделаем его по той же логике, что одиночный ввод.",
            reply_markup=menu_kb(),
        )
        return True

    if state.get("screen") == "open_notices":
        if text.startswith("✅ Уведомление #"):
            try:
                notice_id = int(text.split("#", 1)[1].split()[0])
                result = core.confirm_cash_notice(notice_id, operator_id=int(user_id), operator_note="Подтверждено через Telegram касса v2")
                await update.message.reply_text(
                    "✅ Уведомление подтверждено.\n"
                    f"Чек: {result.get('receipt_number')}\n"
                    f"Payment ID: {result.get('payment_id')}",
                    reply_markup=menu_kb(),
                )
            except Exception as e:
                await update.message.reply_text("⚠ Ошибка подтверждения:\n" + str(e), reply_markup=menu_kb())
            return True

    if state.get("screen") == "cash_type":
        draft = state.get("draft") or {}
        if text == BTN_NIGHT:
            draft["service_group"] = "night"
            await ask_period(update, user_states, user_id, draft)
            return True
        if text == BTN_DAY:
            draft["service_group"] = "day"
            await ask_period(update, user_states, user_id, draft)
            return True
        if text == BTN_MISC:
            await choose_service_group(update, user_states, user_id, draft)
            return True
        await update.message.reply_text("Выберите Night, Day или Другое.", reply_markup=cash_type_kb())
        return True

    if state.get("screen") == "misc_group":
        draft = state.get("draft") or {}
        mapping = {
            BTN_ACTUAL_FEE: "actual",
            BTN_REMOTES: "remote",
            BTN_PHONE: "phone",
            BTN_COMMON_FEES: "common",
            BTN_PARKING_PLACES: "parking_place",
            BTN_COMMERCIAL: "commercial",
            BTN_TEST_SERVICES: "test",
        }
        group = mapping.get(text)
        if not group:
            await update.message.reply_text("Выберите группу кнопкой.", reply_markup=misc_group_kb())
            return True
        draft["service_group"] = group
        await ask_period(update, user_states, user_id, draft)
        return True

    if state.get("screen") == "period":
        draft = state.get("draft") or {}
        if text == BTN_CUSTOM_PERIOD:
            user_states[user_id] = {"mode": "cashier_v2", "screen": "custom_period", "draft": draft}
            await update.message.reply_text("Введите период в формате ГГГГ-ММ:", reply_markup=back_kb())
            return True
        if text == BTN_NO_PERIOD:
            draft["period_code"] = None
        elif text in suggested_periods():
            draft["period_code"] = text
        else:
            await update.message.reply_text("Выберите период кнопкой.", reply_markup=period_kb())
            return True
        await show_services(update, user_states, user_id, draft, draft.get("service_group") or "actual")
        return True

    if state.get("screen") == "custom_period":
        draft = state.get("draft") or {}
        try:
            draft["period_code"] = core.normalize_period(text)
        except Exception:
            await update.message.reply_text("⚠ Не понял период. Пример: 2026-07", reply_markup=back_kb())
            return True
        await show_services(update, user_states, user_id, draft, draft.get("service_group") or "actual")
        return True

    if state.get("screen") == "service":
        try:
            idx = int(text.split(".", 1)[0]) - 1
        except Exception:
            await update.message.reply_text("Выберите услугу кнопкой.", reply_markup=service_kb(state.get("service_options") or []))
            return True
        options = state.get("service_options") or []
        if idx < 0 or idx >= len(options):
            await update.message.reply_text("Такой услуги нет в списке.", reply_markup=service_kb(options))
            return True
        draft = state.get("draft") or {}
        draft["service"] = options[idx]
        await ask_payer(update, user_states, user_id, draft)
        return True

    if state.get("screen") == "payer_query":
        draft = state.get("draft") or {}
        items = find_payers(text)
        if not items:
            await update.message.reply_text("⚠ Не нашёл квартиру или автомобиль.", reply_markup=back_kb())
            return True
        if len(items) == 1:
            draft["payer"] = items[0]
            await ask_amount(update, user_states, user_id, draft)
            return True
        user_states[user_id] = {"mode": "cashier_v2", "screen": "payer_select", "draft": draft, "payer_options": items}
        await update.message.reply_text("Найдено несколько вариантов. Выберите:", reply_markup=payer_kb(items))
        return True

    if state.get("screen") == "payer_select":
        try:
            idx = int(text.split(".", 1)[0]) - 1
        except Exception:
            await update.message.reply_text("Выберите плательщика кнопкой.", reply_markup=payer_kb(state.get("payer_options") or []))
            return True
        options = state.get("payer_options") or []
        if idx < 0 or idx >= len(options):
            await update.message.reply_text("Такого варианта нет.", reply_markup=payer_kb(options))
            return True
        draft = state.get("draft") or {}
        draft["payer"] = options[idx]
        await ask_amount(update, user_states, user_id, draft)
        return True

    if state.get("screen") == "amount":
        amount = parse_amount(text)
        if amount is None:
            await update.message.reply_text("Введите сумму числом, например 400 или 400,50.", reply_markup=back_kb())
            return True
        draft = state.get("draft") or {}
        draft["amount"] = amount
        await ask_source(update, user_states, user_id, draft)
        return True

    if state.get("screen") == "source":
        if not text or text in {"-", "—"}:
            await update.message.reply_text("Основание обязательно.", reply_markup=back_kb())
            return True
        draft = state.get("draft") or {}
        draft["source_text"] = text
        user_states[user_id] = {"mode": "cashier_v2", "screen": "confirm", "draft": draft}
        await update.message.reply_text(draft_text(draft), reply_markup=confirm_kb())
        return True

    if state.get("screen") == "confirm":
        if text != BTN_CONFIRM:
            await update.message.reply_text("Нажмите «Подтвердить» или «Отмена».", reply_markup=confirm_kb())
            return True

        draft = state.get("draft") or {}
        conn = core.get_conn()
        try:
            cur = conn.cursor()
            result = core.create_cash_receipt(
                cur,
                apartment=payer_to_apartment(draft["payer"]),
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
