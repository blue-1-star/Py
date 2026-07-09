#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import re
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

import cashier_v2_core as core

BTN_PAYMENTS = "💳 Платежи"
BTN_CASHIER_V2 = "💰 Касса v2"
BTN_CASH = "💵 Наличные"
BTN_SUMMARY = "📊 Сводка кассы"
BTN_LAST_RECEIPTS = "📜 Последние чеки"
BTN_OPEN_NOTICES = "📨 Уведомления жителей"
BTN_SETTINGS = "⚙️ Настройки кассы"

BTN_NIGHT = "🌙 Night"
BTN_DAY = "☀️ Day"
BTN_MISC = "📦 Другое"

BTN_ACTUAL = "📌 Актуальный сбор"
BTN_REMOTES = "🔑 Пульты"
BTN_PHONE = "📞 Телефонный доступ"
BTN_COMMON = "🧰 Общие сборы"
BTN_PARKING_PLACES = "🅿️ Паркоместа"
BTN_COMMERCIAL = "🏢 Коммерческие"
BTN_TEST = "🧪 Тестовые услуги"

BTN_ACTIVE_SETTING = "📌 Настроить актуальный сбор"
BTN_CONFIRM = "✅ Подтвердить"
BTN_CANCEL = "❌ Отмена"
BTN_BACK = "⬅️ К кассе"
BTN_MAIN = "🏠 Главное меню"
BTN_NEXT = "➕ Следующая оплата"
BTN_RECEIPT = "🧾 Показать чек"
BTN_CUSTOM_PERIOD = "📅 Другой период"
BTN_NO_PERIOD = "❔ Без периода"

SETTING_ACTIVE_COLLECTION = "active_collection_service_item_code"
DEFAULT_CASHBOX_CODE = "O"
MAX_SERVICE_BUTTONS = 12


def kb(rows: list[list[str]]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def service_code_of(opt: dict) -> str | None:
    for key in ("service_item_code", "service_code", "base_service_code", "code"):
        if opt.get(key):
            return str(opt.get(key))
    return None


def setting_get(key: str) -> str | None:
    conn = core.get_conn()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cashier_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            )
        """)
        row = conn.execute("SELECT setting_value FROM cashier_settings WHERE setting_key=?", (key,)).fetchone()
        return row[0] if row and row[0] else None
    finally:
        conn.close()


def setting_set(key: str, value: str, note: str | None = None) -> None:
    conn = core.get_conn()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cashier_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            )
        """)
        conn.execute("""
            INSERT INTO cashier_settings(setting_key, setting_value, note, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(setting_key) DO UPDATE SET
                setting_value=excluded.setting_value,
                note=excluded.note,
                updated_at=CURRENT_TIMESTAMP
        """, (key, value, note))
        conn.commit()
    finally:
        conn.close()


def money(value: Any) -> str:
    try:
        return f"{float(value):.2f}"
    except Exception:
        return "0.00"


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


def period_display(period: str | None) -> str:
    if not period:
        return "—"
    m = re.match(r"^(\d{4})-(\d{2})$", str(period))
    return f"{m.group(2)}-{m.group(1)}" if m else str(period)


def period_storage(text: str) -> str:
    value = text.strip()
    m = re.match(r"^(\d{2})-(\d{4})$", value)
    if m:
        return f"{m.group(2)}-{m.group(1)}"
    return core.normalize_period(value)


def default_period() -> str:
    today = date.today()
    delta = 0 if today.day <= 15 else 1
    y, m = month_add(today.year, today.month, delta)
    return period_code(y, m)


def suggested_periods() -> list[str]:
    y, m = map(int, default_period().split("-"))
    return [period_code(*month_add(y, m, d)) for d in (-2, -1, 0, 1)]


def menu_kb() -> ReplyKeyboardMarkup:
    return kb([
        [BTN_CASH],
        [BTN_OPEN_NOTICES, BTN_LAST_RECEIPTS],
        [BTN_SUMMARY],
        [BTN_SETTINGS],
        [BTN_BACK, BTN_MAIN],
    ])


def cash_type_kb() -> ReplyKeyboardMarkup:
    return kb([[BTN_NIGHT, BTN_DAY], [BTN_MISC], [BTN_BACK, BTN_MAIN]])


def period_kb() -> ReplyKeyboardMarkup:
    p = [period_display(x) for x in suggested_periods()]
    return kb([[p[0], p[1]], [p[2], p[3]], [BTN_CUSTOM_PERIOD, BTN_NO_PERIOD], [BTN_BACK, BTN_MAIN]])


def back_kb() -> ReplyKeyboardMarkup:
    return kb([[BTN_BACK, BTN_MAIN]])


def confirm_kb() -> ReplyKeyboardMarkup:
    return kb([[BTN_CONFIRM], [BTN_CANCEL]])


def settings_kb() -> ReplyKeyboardMarkup:
    return kb([[BTN_ACTIVE_SETTING], [BTN_BACK, BTN_MAIN]])


def option_text(opt: dict) -> str:
    keys = ("service_item_code", "base_service_code", "service_code", "service_type", "display_name", "service_name", "name", "label", "title", "public_name_uk", "public_name_ru", "description")
    return " ".join(str(opt.get(k) or "") for k in keys).lower()


def service_label(opt: dict) -> str:
    try:
        label = core.service_label(opt)
    except Exception:
        label = str(opt)
    return label.replace("ТЕСТ — ", "").replace("TEST — ", "").strip()


def is_test_service(opt: dict) -> bool:
    t = option_text(opt)
    return "test" in t or "тест" in t


def all_services(period: str | None) -> list[dict]:
    try:
        return list(core.service_options(period))
    except Exception:
        return []


def active_collection_service(period: str | None = None) -> dict | None:
    code = setting_get(SETTING_ACTIVE_COLLECTION)
    if not code:
        return None
    for candidate_period in (period, default_period(), None):
        for opt in all_services(candidate_period):
            if service_code_of(opt) == code:
                return opt
    return None


def active_collection_button() -> str:
    opt = active_collection_service()
    if not opt:
        return BTN_ACTUAL
    label = service_label(opt)
    if len(label) > 36:
        label = label[:33] + "..."
    return "📌 Актуальный: " + label


def misc_kb() -> ReplyKeyboardMarkup:
    return kb([
        [active_collection_button()],
        [BTN_REMOTES, BTN_PHONE],
        [BTN_COMMON],
        [BTN_PARKING_PLACES],
        [BTN_COMMERCIAL],
        [BTN_TEST],
        [BTN_BACK, BTN_MAIN],
    ])


def service_kb(options: list[dict]) -> ReplyKeyboardMarkup:
    rows = []
    for i, opt in enumerate(options[:MAX_SERVICE_BUTTONS], 1):
        label = service_label(opt)
        rows.append([f"{i}. {label[:56]}"])
    rows.append([BTN_BACK, BTN_MAIN])
    return kb(rows)


def filter_services(period: str | None, group: str) -> list[dict]:
    out = []
    for opt in all_services(period):
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
        elif group == "parking":
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


def parse_amount(text: str) -> float | None:
    try:
        amount = float(text.strip().replace(",", "."))
    except ValueError:
        return None
    return amount if amount > 0 else None


def find_payers(query: str) -> list[dict]:
    q = query.strip()
    results = []

    try:
        kind, units, _ = core.resolve_physical_unit(q)
        if units:
            for u in units[:8]:
                ap = str(u.get("apartment_number") or q)
                results.append({"kind": "apartment", "apartment_number": ap, "apartment": u, "label": f"🏠 квартира {ap}"})
    except Exception:
        pass

    conn = core.get_conn()
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if cur.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='vehicles'").fetchone():
            like = "%" + q.replace(" ", "").upper() + "%"
            rows = cur.execute("""
                SELECT v.*, a.apartment_number
                FROM vehicles v
                LEFT JOIN apartments a ON a.id=v.apartment_id
                WHERE UPPER(REPLACE(COALESCE(v.license_plate,''),' ','')) LIKE ?
                   OR UPPER(REPLACE(COALESCE(v.license_plate_normalized,''),' ','')) LIKE ?
                ORDER BY a.apartment_number, v.license_plate
                LIMIT 8
            """, (like, like)).fetchall()
            for r in rows:
                ap = str(r["apartment_number"] or "")
                plate = r["license_plate"] or r["license_plate_normalized"] or q
                results.append({"kind": "vehicle", "apartment_number": ap, "vehicle_id": r["id"], "plate": plate, "label": f"🚗 {plate} / кв. {ap}"})
    except Exception:
        pass
    finally:
        conn.close()

    unique = []
    seen = set()
    for r in results:
        if r["label"] not in seen:
            seen.add(r["label"])
            unique.append(r)
    return unique[:10]


def payer_kb(items: list[dict]) -> ReplyKeyboardMarkup:
    return kb([[f"{i+1}. {x['label']}"] for i, x in enumerate(items)] + [[BTN_BACK, BTN_MAIN]])


def payer_to_apartment(payer: dict) -> dict:
    return payer.get("apartment") or {"apartment_number": payer.get("apartment_number")}


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


def last_receipts_text() -> str:
    conn = core.get_conn()
    try:
        rows = conn.execute("SELECT * FROM cashier_receipts ORDER BY id DESC LIMIT 7").fetchall()
    finally:
        conn.close()
    if not rows:
        return "📜 Последние чеки\n\nЗаписей нет."
    parts = ["📜 Последние чеки", ""]
    for i, r in enumerate(rows, 1):
        parts.append(
            f"{i}. Чек #{r['id']} / {r['receipt_number']}\n"
            f"Квартира: {r['apartment_number'] or '—'}\n"
            f"Дата: {r['receipt_date'] or '—'}\n"
            f"Сумма: {money(r['amount'])} {r['currency'] or 'UAH'}\n"
            f"Услуга: {r['service_item_code'] or r['service_hint'] or '—'}"
        )
        parts.append("────────────────")
    return "\n".join(parts).rstrip("─\n")


def draft_text(d: dict[str, Any]) -> str:
    return (
        "💰 Принять наличные\n\n"
        f"Плательщик: {(d.get('payer') or {}).get('label') or '—'}\n"
        f"Квартира: {(d.get('payer') or {}).get('apartment_number') or '—'}\n"
        f"Сумма: {money(d.get('amount'))} UAH\n"
        f"Период: {period_display(d.get('period_code'))}\n"
        f"Услуга: {service_label(d.get('service') or {})}\n"
        f"Основание: {d.get('source_text') or '—'}\n\n"
        "Сохранить чек и оплату?"
    )


async def show_cashier_v2(update: Update, user_states: dict[int, Any], user_id: int) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "menu"}
    await update.message.reply_text(
        "💰 Касса и платежи v2\n\n"
        "Рабочий сценарий: наличные → тип оплаты → период → плательщик → сумма → подтверждение.",
        reply_markup=menu_kb(),
    )


async def start_cash(update: Update, user_states: dict[int, Any], user_id: int) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "cash_type", "draft": {"cashbox_code": DEFAULT_CASHBOX_CODE}}
    await update.message.reply_text("💵 Наличные\n\nВыберите тип оплаты:", reply_markup=cash_type_kb())


async def ask_period(update: Update, user_states: dict[int, Any], user_id: int, draft: dict[str, Any]) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "period", "draft": draft}
    await update.message.reply_text(f"Выберите период оплаты.\nПериод по умолчанию: {period_display(default_period())}", reply_markup=period_kb())


async def choose_misc(update: Update, user_states: dict[int, Any], user_id: int, draft: dict[str, Any]) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "misc_group", "draft": draft}
    await update.message.reply_text("📦 Другое\n\nВыберите группу услуги:", reply_markup=misc_kb())


async def show_services(update: Update, user_states: dict[int, Any], user_id: int, draft: dict[str, Any], group: str) -> None:
    if group == "actual":
        active = active_collection_service(draft.get("period_code"))
        if active:
            draft["service"] = active
            await ask_payer(update, user_states, user_id, draft)
            return
    options = filter_services(draft.get("period_code"), group)
    if not options:
        await update.message.reply_text("⚠ Для этой группы услуги не найдены.", reply_markup=menu_kb())
        return
    user_states[user_id] = {"mode": "cashier_v2", "screen": "service", "draft": draft, "service_options": options[:MAX_SERVICE_BUTTONS]}
    await update.message.reply_text("Выберите услугу:", reply_markup=service_kb(options))


async def ask_payer(update: Update, user_states: dict[int, Any], user_id: int, draft: dict[str, Any]) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "payer_query", "draft": draft}
    await update.message.reply_text(
        "🔍 Найдите плательщика\n\nВведите номер квартиры или несколько цифр госномера автомобиля.\n\nНапример: 174 или 8821.",
        reply_markup=back_kb(),
    )


async def ask_amount(update: Update, user_states: dict[int, Any], user_id: int, draft: dict[str, Any]) -> None:
    user_states[user_id] = {"mode": "cashier_v2", "screen": "amount", "draft": draft}
    await update.message.reply_text("Введите сумму оплаты:", reply_markup=back_kb())


async def handle_cashier_v2_text(update: Update, context: ContextTypes.DEFAULT_TYPE, user_states: dict[int, Any], user_id: int) -> bool:
    text = (update.message.text or "").strip()
    state = user_states.get(user_id, {})

    if state.get("mode") != "cashier_v2" and text not in {BTN_PAYMENTS, BTN_CASHIER_V2, "💰 Касса"}:
        return False

    if text in {BTN_PAYMENTS, BTN_CASHIER_V2, "💰 Касса"}:
        await show_cashier_v2(update, user_states, user_id)
        return True

    if text == BTN_MAIN:
        user_states[user_id] = {}
        await update.message.reply_text("🏠 Главное меню")
        return True
    if text in {BTN_BACK, BTN_CANCEL}:
        await show_cashier_v2(update, user_states, user_id)
        return True

    if text == BTN_CASH:
        await start_cash(update, user_states, user_id)
        return True
    if text == BTN_NEXT:
        await start_cash(update, user_states, user_id)
        return True
    if text == BTN_SUMMARY:
        await update.message.reply_text(summary_text(), reply_markup=menu_kb())
        return True
    if text == BTN_LAST_RECEIPTS:
        await update.message.reply_text(last_receipts_text(), reply_markup=menu_kb())
        return True
    if text == BTN_OPEN_NOTICES:
        await update.message.reply_text("📨 Уведомления жителей\n\nЭтот режим оставлен в ядре кассы, но в v0.3 основной путь — прямая оплата наличными.", reply_markup=menu_kb())
        return True
    if text == BTN_SETTINGS:
        active = active_collection_service()
        msg = "⚙️ Настройки кассы\n\n📌 Актуальный сбор: " + (service_label(active) if active else "не выбран")
        user_states[user_id] = {"mode": "cashier_v2", "screen": "settings"}
        await update.message.reply_text(msg, reply_markup=settings_kb())
        return True
    if text == BTN_ACTIVE_SETTING:
        options = [x for x in all_services(default_period()) if not is_test_service(x)]
        user_states[user_id] = {"mode": "cashier_v2", "screen": "set_active", "service_options": options[:MAX_SERVICE_BUTTONS]}
        await update.message.reply_text("📌 Выберите услугу для кнопки «Актуальный сбор»:", reply_markup=service_kb(options))
        return True

    if state.get("screen") == "set_active":
        try:
            idx = int(text.split(".", 1)[0]) - 1
            opt = (state.get("service_options") or [])[idx]
        except Exception:
            await update.message.reply_text("Выберите услугу кнопкой.", reply_markup=service_kb(state.get("service_options") or []))
            return True
        code = service_code_of(opt)
        if not code:
            await update.message.reply_text("⚠ У услуги нет кода.", reply_markup=settings_kb())
            return True
        setting_set(SETTING_ACTIVE_COLLECTION, code, service_label(opt))
        await update.message.reply_text("✅ Актуальный сбор установлен:\n\n" + service_label(opt), reply_markup=settings_kb())
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
            await choose_misc(update, user_states, user_id, draft)
            return True
        await update.message.reply_text("Выберите Night, Day или Другое.", reply_markup=cash_type_kb())
        return True

    if state.get("screen") == "misc_group":
        draft = state.get("draft") or {}
        mapping = {
            BTN_ACTUAL: "actual",
            active_collection_button(): "actual",
            BTN_REMOTES: "remote",
            BTN_PHONE: "phone",
            BTN_COMMON: "common",
            BTN_PARKING_PLACES: "parking",
            BTN_COMMERCIAL: "commercial",
            BTN_TEST: "test",
        }
        group = mapping.get(text)
        if not group:
            await update.message.reply_text("Выберите группу кнопкой.", reply_markup=misc_kb())
            return True
        draft["service_group"] = group
        await ask_period(update, user_states, user_id, draft)
        return True

    if state.get("screen") == "period":
        draft = state.get("draft") or {}
        if text == BTN_CUSTOM_PERIOD:
            user_states[user_id] = {"mode": "cashier_v2", "screen": "custom_period", "draft": draft}
            await update.message.reply_text("Введите период, например 06-2026 или 2026-06:", reply_markup=back_kb())
            return True
        if text == BTN_NO_PERIOD:
            draft["period_code"] = None
        else:
            try:
                storage = period_storage(text)
            except Exception:
                await update.message.reply_text("Выберите период кнопкой.", reply_markup=period_kb())
                return True
            if storage not in suggested_periods():
                await update.message.reply_text("Выберите период кнопкой.", reply_markup=period_kb())
                return True
            draft["period_code"] = storage
        await show_services(update, user_states, user_id, draft, draft.get("service_group") or "actual")
        return True

    if state.get("screen") == "custom_period":
        draft = state.get("draft") or {}
        try:
            draft["period_code"] = period_storage(text)
        except Exception:
            await update.message.reply_text("⚠ Не понял период.", reply_markup=back_kb())
            return True
        await show_services(update, user_states, user_id, draft, draft.get("service_group") or "actual")
        return True

    if state.get("screen") == "service":
        try:
            idx = int(text.split(".", 1)[0]) - 1
            opt = (state.get("service_options") or [])[idx]
        except Exception:
            await update.message.reply_text("Выберите услугу кнопкой.", reply_markup=service_kb(state.get("service_options") or []))
            return True
        draft = state.get("draft") or {}
        draft["service"] = opt
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
        await update.message.reply_text("Найдено несколько вариантов:", reply_markup=payer_kb(items))
        return True

    if state.get("screen") == "payer_select":
        try:
            idx = int(text.split(".", 1)[0]) - 1
            payer = (state.get("payer_options") or [])[idx]
        except Exception:
            await update.message.reply_text("Выберите плательщика кнопкой.", reply_markup=payer_kb(state.get("payer_options") or []))
            return True
        draft = state.get("draft") or {}
        draft["payer"] = payer
        await ask_amount(update, user_states, user_id, draft)
        return True

    if state.get("screen") == "amount":
        amount = parse_amount(text)
        if amount is None:
            await update.message.reply_text("Введите сумму числом, например 400 или 400,50.", reply_markup=back_kb())
            return True
        draft = state.get("draft") or {}
        draft["amount"] = amount
        user_states[user_id] = {"mode": "cashier_v2", "screen": "source", "draft": draft}
        await update.message.reply_text("Введите основание/комментарий:", reply_markup=back_kb())
        return True

    if state.get("screen") == "source":
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
                source_text=draft.get("source_text") or "Telegram cashier v0.3",
                operator_id=int(user_id),
                origin_kind="HAND_TO_HAND",
            )
            conn.commit()
            user_states[user_id] = {"mode": "cashier_v2", "screen": "after_success", "last_result": result}
            await update.message.reply_text(
                "✅ Оплата принята\n\n"
                f"Период: {period_display(draft.get('period_code'))}\n"
                f"Сумма: {money(draft.get('amount'))} UAH\n"
                f"Чек: {result.get('receipt_number')}\n"
                f"Payment ID: {result.get('payment_id')}",
                reply_markup=kb([[BTN_NEXT], [BTN_RECEIPT], [BTN_BACK, BTN_MAIN]]),
            )
        except Exception as e:
            conn.rollback()
            await update.message.reply_text("⚠ Ошибка сохранения:\n" + str(e), reply_markup=menu_kb())
        finally:
            conn.close()
        return True

    if text == BTN_RECEIPT:
        result = state.get("last_result") or {}
        await update.message.reply_text(
            "🧾 Чек\n\n"
            f"Номер: {result.get('receipt_number') or '—'}\n"
            f"Receipt ID: {result.get('receipt_id') or '—'}\n"
            f"Payment ID: {result.get('payment_id') or '—'}",
            reply_markup=menu_kb(),
        )
        return True

    return False
