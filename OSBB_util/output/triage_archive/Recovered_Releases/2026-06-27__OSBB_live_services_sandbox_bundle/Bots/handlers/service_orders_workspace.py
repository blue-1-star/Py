"""
Интерфейс Telegram для общего контура услуг ОСББ.

Обслуживает две независимые рабочие поверхности:
1) житель — «🔑 Пульты и доступ»;
2) сотрудник с отдельными правами — «🔑 Оператор услуг».

Критические правила:
- заявка не является оплатой;
- уведомление о передаче денег не является подтверждённой оплатой;
- подтверждённый платёж привязывается к конкретной заявке отдельно;
- физический пульт, складской резерв, перепрошивка, выдача и телефонный
  доступ выполняются отдельными шагами с аудитом;
- стандартные действия не требуют свободного текста; ввод нужен только для
  маркировки физического пульта и телефонного номера.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import sqlite3
import sys
from typing import Any

from telegram import ReplyKeyboardMarkup, Update

HANDLERS_DIR = Path(__file__).resolve().parent
BOTS_DIR = HANDLERS_DIR.parent
ROOT = BOTS_DIR.parent
for folder in (ROOT, BOTS_DIR):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))

from access_control import has_permission, write_access_audit
from cashier_v2_core import create_payment_notice
from handlers import client_portal as resident_portal
from service_orders_core import (
    activate_access_credential,
    create_remote_asset,
    create_service_order,
    effective_price,
    get_conn,
    get_service_order,
    link_payment_to_order,
    money,
    record_remote_movement,
    service_order_summary,
    text,
)


MODULE = "service_orders_ui"
OPERATOR_MODE = "service_operator"
OPERATOR_MODE_BUTTON = "🔑 Оператор услуг"
CLIENT_ENTRY_BUTTON = "🔑 Пульты и доступ"
HOME = "🏠 Главное меню"
BACK = "⬅️ К услугам"


I18N = {
    "ru": {
        "title": "🔑 Пульты и доступ",
        "intro": (
            "Заявка, деньги и физический пульт учитываются отдельно.\n"
            "Пульт не выдаётся автоматически после заявки или сообщения об оплате."
        ),
        "reprogram": "♻️ Перепрошить мой пульт",
        "new_remote": "🆕 Получить новый пульт",
        "refurbished": "🔄 Получить восстановленный пульт",
        "phone": "📱 Подключить телефон",
        "my_orders": "📋 Мои заявки",
        "back_portal": "⬅️ В кабинет",
        "order_preview": "📄 Подтверждение заявки",
        "send_order": "✅ Отправить заявку",
        "cancel": "❌ Отменить",
        "order_saved": "✅ Заявка зарегистрирована.",
        "no_unit": "Сначала привяжите квартиру в личном кабинете.",
        "no_offers": "Для жителей пока нет активных услуг пультов и доступа.",
        "my_orders_title": "📋 Мои заявки на пульты и доступ",
        "no_orders": "Заявок пока нет.",
        "cash_notice": "💵 Передал наличные в O",
        "bank_notice": "🏦 Сообщить об оплате через банк",
        "notice_saved": (
            "✅ Уведомление {number} зарегистрировано.\n"
            "Это ещё не оплата: касса или финансовый оператор должны подтвердить поступление."
        ),
        "operator_title": "🔑 Оператор услуг",
        "operator_intro": (
            "Здесь заявки проходят по шагам: деньги ↔ услуга / пульт / цифровой доступ.\n"
            "Ни выдача, ни активация не выполняются автоматически."
        ),
        "open_orders": "📋 Открытые заявки",
        "inventory": "📦 Остатки пультов",
        "refresh": "🔄 Обновить",
        "no_operator_orders": "Нет открытых заявок в доступной вам области.",
        "no_stock": "Нет доступных пультов этого типа.",
        "receive_remote": "📥 Принять пульт жильца",
        "reserve_remote": "📦 Зарезервировать пульт",
        "link_payment": "💳 Привязать оплату",
        "program_done": "🛠 Перепрошивка выполнена",
        "return_remote": "📤 Вернуть пульт жильцу",
        "issue_remote": "📤 Выдать пульт жильцу",
        "activate_phone": "📱 Активировать телефонный доступ",
        "asset_prompt": (
            "Введите маркировку принятого пульта.\n\n"
            "Используйте серийный номер, если он есть. Иначе создайте понятную "
            "метку, например OLD-174-01."
        ),
        "phone_prompt": "Введите телефон для доступа к шлагбауму, например +380501234567.",
        "wrong_phone": "Укажите номер: от 8 до 20 цифр, можно начать с +.",
        "no_payments": (
            "Подтверждённых оплат по этой квартире и услуге пока нет.\n"
            "Сначала житель должен сообщить о передаче денег, а касса / финансовый "
            "оператор — подтвердить фактическое поступление."
        ),
        "choose_payment": "Выберите подтверждённую оплату для этой заявки.",
        "choose_stock": "Выберите конкретный физический пульт из доступного остатка.",
        "denied": "⛔ Нет права на этот раздел или действие.",
        "wrong": "Выберите действие кнопкой.",
        "completed": "✅ Заявка завершена.",
    },
    "uk": {
        "title": "🔑 Пульти та доступ",
        "intro": (
            "Заявка, гроші та фізичний пульт обліковуються окремо.\n"
            "Пульт не видається автоматично після заявки або повідомлення про оплату."
        ),
        "reprogram": "♻️ Перепрограмувати мій пульт",
        "new_remote": "🆕 Отримати новий пульт",
        "refurbished": "🔄 Отримати відновлений пульт",
        "phone": "📱 Підключити телефон",
        "my_orders": "📋 Мої заявки",
        "back_portal": "⬅️ До кабінету",
        "order_preview": "📄 Підтвердження заявки",
        "send_order": "✅ Надіслати заявку",
        "cancel": "❌ Скасувати",
        "order_saved": "✅ Заявку зареєстровано.",
        "no_unit": "Спочатку прив’яжіть квартиру в особистому кабінеті.",
        "no_offers": "Для мешканців поки немає активних послуг пультів і доступу.",
        "my_orders_title": "📋 Мої заявки на пульти та доступ",
        "no_orders": "Заявок поки немає.",
        "cash_notice": "💵 Передав готівку в O",
        "bank_notice": "🏦 Повідомити про оплату через банк",
        "notice_saved": (
            "✅ Повідомлення {number} зареєстровано.\n"
            "Це ще не оплата: каса або фінансовий оператор мають підтвердити надходження."
        ),
        "operator_title": "🔑 Оператор послуг",
        "operator_intro": (
            "Тут заявки проходять кроки: гроші ↔ послуга / пульт / цифровий доступ.\n"
            "Ані видача, ані активація не виконуються автоматично."
        ),
        "open_orders": "📋 Відкриті заявки",
        "inventory": "📦 Залишки пультів",
        "refresh": "🔄 Оновити",
        "no_operator_orders": "Немає відкритих заявок у доступній вам області.",
        "no_stock": "Немає доступних пультів цього типу.",
        "receive_remote": "📥 Прийняти пульт мешканця",
        "reserve_remote": "📦 Зарезервувати пульт",
        "link_payment": "💳 Прив’язати оплату",
        "program_done": "🛠 Перепрограмування виконано",
        "return_remote": "📤 Повернути пульт мешканцю",
        "issue_remote": "📤 Видати пульт мешканцю",
        "activate_phone": "📱 Активувати телефонний доступ",
        "asset_prompt": (
            "Введіть маркування прийнятого пульта.\n\n"
            "Використайте серійний номер, якщо він є. Інакше створіть зрозумілу "
            "мітку, наприклад OLD-174-01."
        ),
        "phone_prompt": "Введіть телефон для доступу до шлагбаума, наприклад +380501234567.",
        "wrong_phone": "Вкажіть номер: від 8 до 20 цифр, можна почати з +.",
        "no_payments": (
            "Підтверджених оплат за цією квартирою та послугою поки немає.\n"
            "Спочатку мешканець має повідомити про передачу грошей, а каса / "
            "фінансовий оператор — підтвердити фактичне надходження."
        ),
        "choose_payment": "Оберіть підтверджену оплату для цієї заявки.",
        "choose_stock": "Оберіть конкретний фізичний пульт із доступного залишку.",
        "denied": "⛔ Немає права на цей розділ або дію.",
        "wrong": "Оберіть дію кнопкою.",
        "completed": "✅ Заявку завершено.",
    },
    "en": {
        "title": "🔑 Remotes and access",
        "intro": "Orders, money and the physical remote are recorded separately.",
        "reprogram": "♻️ Reprogram my remote",
        "new_remote": "🆕 Get a new remote",
        "refurbished": "🔄 Get a refurbished remote",
        "phone": "📱 Connect phone access",
        "my_orders": "📋 My orders",
        "back_portal": "⬅️ Back to portal",
        "order_preview": "📄 Order confirmation",
        "send_order": "✅ Submit order",
        "cancel": "❌ Cancel",
        "order_saved": "✅ Order registered.",
        "no_unit": "Link your apartment in the resident portal first.",
        "no_offers": "No active remote or access services are available yet.",
        "my_orders_title": "📋 My remote and access orders",
        "no_orders": "No orders yet.",
        "cash_notice": "💵 I handed cash to O",
        "bank_notice": "🏦 Report a bank payment",
        "notice_saved": "✅ Notice {number} registered. This is not a payment yet.",
        "operator_title": "🔑 Service operator",
        "operator_intro": "Each order follows separate money and fulfilment steps.",
        "open_orders": "📋 Open orders",
        "inventory": "📦 Remote stock",
        "refresh": "🔄 Refresh",
        "no_operator_orders": "No open orders in your permitted area.",
        "no_stock": "No remotes of this type are available.",
        "receive_remote": "📥 Receive resident remote",
        "reserve_remote": "📦 Reserve remote",
        "link_payment": "💳 Link payment",
        "program_done": "🛠 Reprogramming done",
        "return_remote": "📤 Return remote",
        "issue_remote": "📤 Issue remote",
        "activate_phone": "📱 Activate phone access",
        "asset_prompt": "Enter the remote label or serial number.",
        "phone_prompt": "Enter the phone number for barrier access.",
        "wrong_phone": "Use 8–20 digits; a leading + is allowed.",
        "no_payments": "No matching confirmed payment is available yet.",
        "choose_payment": "Choose confirmed payment for this order.",
        "choose_stock": "Choose a specific physical remote from stock.",
        "denied": "⛔ You do not have permission for this action.",
        "wrong": "Choose an action using the buttons.",
        "completed": "✅ Order completed.",
    },
}

PROFILE_TO_KEY = {
    "REMOTE_REPROGRAM_OWN": "reprogram",
    "REMOTE_NEW_FROM_STOCK": "new_remote",
    "REMOTE_REFURBISHED_FROM_STOCK": "refurbished",
    "PHONE_ACCESS_CONNECT": "phone",
}

STATUS_LABELS = {
    "REQUESTED": "🟡 Нова",
    "AWAITING_RESIDENT_ASSET": "📥 Очікує пульт",
    "AWAITING_STOCK": "📦 Очікує резерв",
    "AWAITING_PAYMENT": "💳 Очікує оплату",
    "IN_PROGRESS": "🛠 У роботі",
    "READY_FOR_ISSUE": "📤 Готово до видачі",
    "COMPLETED": "✅ Завершено",
    "CANCELLED": "⚪ Скасовано",
}
STEP_STATUS = {
    "WAITING": "⏳",
    "CONFIRMED": "✅",
    "WAIVED": "➖",
}


def tr(lang: str, key: str, **kwargs: Any) -> str:
    return I18N.get(lang, I18N["ru"]).get(key, I18N["ru"][key]).format(**kwargs)


def kb(rows: list[list[str]]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def _state(user_states: dict, user_id: int, *, create: bool = False) -> dict | None:
    value = user_states.get(user_id)
    if isinstance(value, dict) and value.get("_module") == MODULE:
        return value
    if create:
        value = {"_module": MODULE, "area": "", "mode": ""}
        user_states[user_id] = value
        return value
    return None


def _home_text(message_text: str) -> bool:
    return text(message_text) in {
        "🏠 Главное меню",
        "🏠 Головне меню",
        "🏠 Main menu",
        "⬅️ Назад",
    }


def _service_back_text(message_text: str) -> bool:
    return text(message_text) in {
        BACK,
        "⬅️ До послуг",
        "⬅️ Back to services",
    }


def _operator_back_text(message_text: str) -> bool:
    return text(message_text) in {
        "⬅️ К оператору",
        "⬅️ До оператора",
        "⬅️ Back to operator",
    }


def _operator_action_texts(lang: str) -> dict[str, str]:
    return {
        "receive_remote": tr(lang, "receive_remote"),
        "reserve_remote": tr(lang, "reserve_remote"),
        "link_payment": tr(lang, "link_payment"),
        "program_done": tr(lang, "program_done"),
        "return_remote": tr(lang, "return_remote"),
        "issue_remote": tr(lang, "issue_remote"),
        "activate_phone": tr(lang, "activate_phone"),
    }


def _resident_entry_texts() -> set[str]:
    values = {CLIENT_ENTRY_BUTTON, "🔑 Пульти та доступ", "🔑 Remotes and access"}
    # Fallback for an old menu while the v3 resident menu is being installed.
    values.update({
        "🔑 Пульты", "🔑 Пульти", "🔑 Remotes",
        "📞 Открытие по телефону", "📞 Відкриття телефоном", "📞 Phone gate access",
    })
    return values


def _operator_mode_texts() -> set[str]:
    return {
        OPERATOR_MODE_BUTTON,
        "🔑 Оператор послуг",
        "🔑 Service operator",
    }


def has_service_workspace_access(user_id: int | str) -> bool:
    return (
        has_permission(
            user_id,
            "service_orders",
            "VIEW",
            scope_type="SERVICE_CATEGORY",
            scope_value="REMOTE",
        )
        or has_permission(
            user_id,
            "service_orders",
            "VIEW",
            scope_type="SERVICE_CATEGORY",
            scope_value="ACCESS",
        )
    )


def _category_allowed(user_id: int | str, category: str, action: str = "VIEW") -> bool:
    return has_permission(
        user_id,
        "service_orders",
        action,
        scope_type="SERVICE_CATEGORY",
        scope_value=text(category).upper() or "GENERAL",
    )


def _account_and_unit(user_id: int) -> dict | None:
    data = resident_portal._account_and_unit(user_id)
    if not data or not data.get("account") or not data.get("unit"):
        return None
    return data


def _current_offers() -> list[dict]:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                i.service_item_code, i.service_code, i.service_item_name,
                i.service_type, i.amount_default, i.currency,
                w.workflow_profile_code, w.resident_request_enabled,
                p.service_category, p.profile_name
            FROM service_items i
            JOIN service_item_workflows w
              ON w.service_item_code = i.service_item_code
             AND w.is_active = 1
            JOIN service_workflow_profiles p
              ON p.profile_code = w.workflow_profile_code
             AND p.is_active = 1
            WHERE COALESCE(i.is_active, 1) = 1
              AND COALESCE(i.status, 'active') = 'active'
              AND w.resident_request_enabled = 1
              AND p.service_category IN ('REMOTE', 'ACCESS')
            ORDER BY p.service_category, i.service_item_name, i.service_item_code
            """
        )
        rows = [dict(row) for row in cur.fetchall()]
        for row in rows:
            amount, currency = effective_price(cur, row["service_item_code"])
            row["effective_amount"] = amount
            row["effective_currency"] = currency
        return rows
    finally:
        conn.close()


def _resident_offer_buttons(state: dict, lang: str) -> list[list[str]]:
    mapping: dict[str, dict] = {}
    rows: list[list[str]] = []
    known: dict[str, dict] = {}
    extra: list[dict] = []
    for offer in _current_offers():
        profile = text(offer.get("workflow_profile_code"))
        if profile in PROFILE_TO_KEY and profile not in known:
            known[profile] = offer
        else:
            extra.append(offer)

    for profile in (
        "REMOTE_REPROGRAM_OWN",
        "REMOTE_NEW_FROM_STOCK",
        "REMOTE_REFURBISHED_FROM_STOCK",
        "PHONE_ACCESS_CONNECT",
    ):
        offer = known.get(profile)
        if not offer:
            continue
        label = tr(lang, PROFILE_TO_KEY[profile])
        mapping[label] = offer
        rows.append([label])

    for offer in extra:
        base = f"🧩 {offer['service_item_name']}"
        label = base
        idx = 2
        while label in mapping:
            label = f"{base} [{idx}]"
            idx += 1
        mapping[label] = offer
        rows.append([label])

    state["offer_buttons"] = mapping
    rows.append([tr(lang, "my_orders")])
    rows.append([tr(lang, "back_portal"), HOME])
    return rows


def _fmt_amount(amount: Any, currency: str = "UAH") -> str:
    if amount is None:
        return "⚠️ цена не задана"
    return f"{money(amount)} {currency or 'UAH'}"


def _order_step_lines(order: dict) -> list[str]:
    lines = []
    for step in order.get("steps") or []:
        icon = STEP_STATUS.get(text(step.get("step_status")), "•")
        lines.append(f"{icon} {step.get('step_name') or step.get('step_code')}")
    return lines


def _next_waiting_step(order: dict) -> dict | None:
    rows = [
        row for row in order.get("steps") or []
        if int(row.get("is_required") or 0) == 1
        and text(row.get("step_status")) not in {"CONFIRMED", "WAIVED"}
    ]
    return sorted(rows, key=lambda row: (int(row.get("sequence_no") or 0), int(row.get("id") or 0)))[0] if rows else None


def _order_card(order: dict, *, lang: str, title: str = "📄 Заявка") -> str:
    due = order.get("amount_due_snapshot")
    lines = [
        title,
        "",
        f"№: {order.get('order_number')}",
        f"Квартира: {order.get('apartment_number') or '-'}",
        f"Услуга: {order.get('service_name_snapshot') or order.get('service_item_code')}",
        f"Сумма: {_fmt_amount(due, order.get('currency') or 'UAH')}",
        f"Статус: {STATUS_LABELS.get(text(order.get('order_status')), order.get('order_status') or '-')}",
        f"Оплата: {text(order.get('payment_status')) or '-'}",
        "",
        "Шаги:",
        *(_order_step_lines(order) or ["—"]),
    ]
    return "\n".join(lines)


def _resident_order_buttons(order: dict, lang: str) -> list[list[str]]:
    rows: list[list[str]] = []
    next_step = _next_waiting_step(order)
    if next_step and text(next_step.get("step_code")) == "PAYMENT_CONFIRMED":
        rows.append([tr(lang, "cash_notice"), tr(lang, "bank_notice")])
    rows.append([BACK, tr(lang, "my_orders")])
    rows.append([HOME])
    return rows


async def show_resident_services(
    update: Update,
    user_states: dict,
    user_id: int,
    *,
    lang: str,
) -> None:
    data = _account_and_unit(user_id)
    if not data:
        await update.message.reply_text(
            tr(lang, "no_unit"),
            reply_markup=kb([[tr(lang, "back_portal")], [HOME]]),
        )
        return

    state = _state(user_states, user_id, create=True)
    state.clear()
    state.update({
        "_module": MODULE,
        "area": "resident",
        "mode": "resident_home",
        "account": data["account"],
        "unit": data["unit"],
    })
    offers = _current_offers()
    text_body = f"{tr(lang, 'title')}\n\n{tr(lang, 'intro')}"
    if not offers:
        text_body += "\n\n" + tr(lang, "no_offers")
    await update.message.reply_text(
        text_body,
        reply_markup=kb(_resident_offer_buttons(state, lang)),
    )


async def _resident_order_preview(update: Update, state: dict, offer: dict, lang: str) -> None:
    state["mode"] = "resident_preview"
    state["offer"] = offer
    unit = state["unit"]
    price = offer.get("effective_amount")
    lines = [
        tr(lang, "order_preview"),
        "",
        f"Квартира: {unit.get('apartment_number') or '-'}",
        f"Услуга: {offer.get('service_item_name') or offer.get('service_item_code')}",
        f"Стоимость: {_fmt_amount(price, offer.get('effective_currency') or 'UAH')}",
        "",
        "Заявка ещё не является оплатой.",
        "После регистрации деньги и выполнение услуги подтверждаются отдельно.",
    ]
    if price is None:
        lines.append("\n⚠️ Услуга не может быть заказана: в каталоге не задана цена.")
        rows = [[BACK], [HOME]]
    else:
        rows = [[tr(lang, "send_order")], [tr(lang, "cancel"), BACK], [HOME]]
    await update.message.reply_text("\n".join(lines), reply_markup=kb(rows))


def _resident_order_create(state: dict, user_id: int) -> dict:
    account = state["account"]
    unit = state["unit"]
    offer = state["offer"]
    conn = get_conn()
    try:
        order = create_service_order(
            resident_account_id=int(account["id"]),
            telegram_user_id=user_id,
            apartment_id=int(unit["id"]),
            apartment_number=text(unit.get("apartment_number")),
            service_item_code=offer["service_item_code"],
            quantity=1,
            resident_comment="",
            actor_id=None,
            source_context=f"resident_telegram:{user_id}",
            conn=conn,
        )
        cur = conn.cursor()
        # The generic core safely allows a resident-originated request without
        # granting staff rights. Preserve the actual resident as event actor.
        cur.execute(
            """
            UPDATE service_order_events
            SET actor_id = ?
            WHERE id = (
                SELECT id
                FROM service_order_events
                WHERE service_order_id = ?
                  AND event_type = 'ORDER_CREATED'
                ORDER BY id DESC
                LIMIT 1
            )
            """,
            (str(user_id), int(order["id"])),
        )
        write_access_audit(
            conn,
            actor_user_id=user_id,
            action_type="resident_service_order_created",
            resource="service_orders",
            action="CREATE",
            scope_type="UNIT",
            scope_value=text(unit.get("apartment_number")),
            target_table="service_orders",
            target_id=int(order["id"]),
            details=f"resident request {order['order_number']}; {offer['service_item_code']}",
        )
        conn.commit()
        return service_order_summary(int(order["id"]), conn=conn)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _resident_orders(account_id: int) -> list[dict]:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, order_number, apartment_number, service_name_snapshot,
                   service_item_code, order_status, payment_status,
                   fulfillment_status, requested_at
            FROM service_orders
            WHERE resident_account_id = ?
            ORDER BY id DESC
            LIMIT 40
            """,
            (int(account_id),),
        )
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


async def _show_resident_orders(update: Update, state: dict, lang: str) -> None:
    state["mode"] = "resident_orders"
    rows = _resident_orders(int(state["account"]["id"]))
    mapping: dict[str, int] = {}
    buttons: list[list[str]] = []
    lines = [tr(lang, "my_orders_title"), ""]
    for row in rows:
        label = f"📄 {row['order_number']} | {row.get('service_name_snapshot') or row.get('service_item_code')}"
        mapping[label] = int(row["id"])
        buttons.append([label])
        lines.append(
            f"{row['order_number']} | "
            f"{STATUS_LABELS.get(text(row.get('order_status')), row.get('order_status') or '-')} | "
            f"{row.get('service_name_snapshot') or row.get('service_item_code')}"
        )
    if not rows:
        lines.append(tr(lang, "no_orders"))
    state["resident_order_buttons"] = mapping
    buttons.extend([[BACK], [HOME]])
    await update.message.reply_text("\n".join(lines), reply_markup=kb(buttons))


async def _show_resident_order_card(update: Update, state: dict, order_id: int, lang: str) -> None:
    order = service_order_summary(order_id)
    if int(order.get("resident_account_id") or -1) != int(state["account"]["id"]):
        await update.message.reply_text(tr(lang, "denied"))
        return
    state["mode"] = "resident_order_card"
    state["order_id"] = int(order_id)
    await update.message.reply_text(
        _order_card(order, lang=lang, title="📄 Моя заявка"),
        reply_markup=kb(_resident_order_buttons(order, lang)),
    )


def _notice_for_order(order: dict, state: dict, user_id: int, notice_type: str) -> dict:
    due = float(order.get("amount_due_snapshot") or 0)
    if due <= 0:
        raise ValueError("Для заявки не задана положительная сумма.")
    service = {
        "service_code": order.get("service_code") or order.get("service_item_code"),
        "service_item_code": order.get("service_item_code"),
        "service_type": "ONE_TIME",
        "service_name": order.get("service_name_snapshot"),
    }
    return create_payment_notice(
        account=state["account"],
        apartment=state["unit"],
        notice_type=notice_type,
        declared_cashbox_code="O" if notice_type == "CASH_HANDOVER" else None,
        period_code=None,
        service=service,
        amount=due,
        resident_comment=f"Заявка {order.get('order_number')}.",
    )


async def _handle_resident(
    update: Update,
    user_states: dict,
    user_id: int,
    message_text: str,
    *,
    lang: str,
    state: dict,
) -> bool:
    if _home_text(message_text):
        user_states.pop(user_id, None)
        return False

    mode = text(state.get("mode"))
    if _service_back_text(message_text):
        await show_resident_services(update, user_states, user_id, lang=lang)
        return True

    if mode == "resident_home":
        if message_text == tr(lang, "my_orders"):
            await _show_resident_orders(update, state, lang)
            return True
        offer = (state.get("offer_buttons") or {}).get(message_text)
        if offer:
            await _resident_order_preview(update, state, offer, lang)
            return True
        if message_text == tr(lang, "back_portal"):
            user_states.pop(user_id, None)
            return False
        await update.message.reply_text(tr(lang, "wrong"))
        return True

    if mode == "resident_preview":
        if message_text == tr(lang, "send_order"):
            try:
                order = _resident_order_create(state, user_id)
            except Exception as exc:
                await update.message.reply_text(f"⚠️ {exc}")
                return True
            await update.message.reply_text(tr(lang, "order_saved"))
            await _show_resident_order_card(update, state, int(order["id"]), lang)
            return True
        if message_text == tr(lang, "cancel"):
            await show_resident_services(update, user_states, user_id, lang=lang)
            return True
        await update.message.reply_text(tr(lang, "wrong"))
        return True

    if mode == "resident_orders":
        order_id = (state.get("resident_order_buttons") or {}).get(message_text)
        if order_id:
            await _show_resident_order_card(update, state, int(order_id), lang)
            return True
        await update.message.reply_text(tr(lang, "wrong"))
        return True

    if mode == "resident_order_card":
        if message_text in {tr(lang, "cash_notice"), tr(lang, "bank_notice")}:
            order = service_order_summary(int(state["order_id"]))
            notice_type = "CASH_HANDOVER" if message_text == tr(lang, "cash_notice") else "BANK_TRANSFER"
            try:
                notice = _notice_for_order(order, state, user_id, notice_type)
            except Exception as exc:
                await update.message.reply_text(f"⚠️ {exc}")
                return True
            await update.message.reply_text(
                tr(lang, "notice_saved", number=notice["notice_number"])
            )
            await _show_resident_order_card(update, state, int(state["order_id"]), lang)
            return True
        if message_text == tr(lang, "my_orders"):
            await _show_resident_orders(update, state, lang)
            return True
        await update.message.reply_text(tr(lang, "wrong"))
        return True

    await show_resident_services(update, user_states, user_id, lang=lang)
    return True


def _visible_operator_categories(user_id: int) -> set[str]:
    categories = set()
    for category in ("REMOTE", "ACCESS"):
        if _category_allowed(user_id, category, "VIEW"):
            categories.add(category)
    return categories


def _operator_orders(user_id: int) -> list[dict]:
    categories = _visible_operator_categories(user_id)
    if not categories:
        return []
    conn = get_conn()
    try:
        cur = conn.cursor()
        placeholders = ",".join("?" for _ in categories)
        cur.execute(
            f"""
            SELECT
                o.id, o.order_number, o.apartment_number,
                o.service_name_snapshot, o.service_item_code,
                o.order_status, o.payment_status, o.fulfillment_status,
                o.workflow_profile_code, p.service_category,
                o.requested_at
            FROM service_orders o
            JOIN service_workflow_profiles p
              ON p.profile_code = o.workflow_profile_code
            WHERE o.order_status NOT IN ('COMPLETED', 'CANCELLED')
              AND p.service_category IN ({placeholders})
            ORDER BY o.id ASC
            LIMIT 60
            """,
            tuple(sorted(categories)),
        )
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def _order_category(order: dict) -> str:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT p.service_category
            FROM service_workflow_profiles p
            WHERE p.profile_code = ?
            """,
            (order["workflow_profile_code"],),
        )
        row = cur.fetchone()
        return text(row[0]) if row else "GENERAL"
    finally:
        conn.close()


async def show_service_operator_workspace(
    update: Update,
    user_states: dict,
    user_id: int,
    *,
    lang: str,
) -> None:
    if not has_service_workspace_access(user_id):
        await update.message.reply_text(tr(lang, "denied"))
        return
    state = _state(user_states, user_id, create=True)
    state.clear()
    state.update({"_module": MODULE, "area": "operator", "mode": "operator_home"})
    await update.message.reply_text(
        f"{tr(lang, 'operator_title')}\n\n{tr(lang, 'operator_intro')}",
        reply_markup=kb([
            [tr(lang, "open_orders")],
            [tr(lang, "inventory"), tr(lang, "refresh")],
            [HOME],
        ]),
    )


async def _show_operator_orders(update: Update, state: dict, user_id: int, lang: str) -> None:
    state["mode"] = "operator_orders"
    rows = _operator_orders(user_id)
    mapping: dict[str, int] = {}
    buttons: list[list[str]] = []
    lines = [tr(lang, "open_orders"), ""]
    for row in rows:
        label = (
            f"📄 {row['order_number']} | кв.{row.get('apartment_number') or '-'} | "
            f"{row.get('service_name_snapshot') or row.get('service_item_code')}"
        )
        mapping[label] = int(row["id"])
        buttons.append([label])
        lines.append(
            f"{row['order_number']} | кв.{row.get('apartment_number') or '-'} | "
            f"{STATUS_LABELS.get(text(row.get('order_status')), row.get('order_status') or '-')}"
        )
    if not rows:
        lines.append(tr(lang, "no_operator_orders"))
    state["operator_order_buttons"] = mapping
    buttons.extend([["⬅️ К оператору"], [HOME]])
    await update.message.reply_text("\n".join(lines), reply_markup=kb(buttons))


def _assert_operator_order_access(user_id: int, order: dict, action: str = "VIEW") -> str:
    """
    Enforce the permission that corresponds to the actual operation.

    Reading/creating an order uses service_orders; confirming a workflow step
    uses service_order_steps. This keeps the server-side check aligned with
    the narrow role permissions seeded by the migration.
    """
    category = _order_category(order)
    resource = "service_order_steps" if action == "CONFIRM" else "service_orders"
    if not has_permission(
        user_id,
        resource,
        action,
        scope_type="SERVICE_CATEGORY",
        scope_value=category,
    ):
        raise PermissionError("Нет права на заявку этой категории.")
    return category


def _order_remote_details(order_id: int) -> dict:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM remote_order_details WHERE service_order_id = ?",
            (int(order_id),),
        )
        row = cur.fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()


def _operator_order_actions(order: dict, lang: str) -> list[list[str]]:
    next_step = _next_waiting_step(order)
    actions = _operator_action_texts(lang)
    rows: list[list[str]] = []
    if next_step:
        code = text(next_step.get("step_code"))
        action_key = {
            "RESIDENT_REMOTE_RECEIVED": "receive_remote",
            "STOCK_ASSET_RESERVED": "reserve_remote",
            "PAYMENT_CONFIRMED": "link_payment",
            "REMOTE_PROGRAMMED": "program_done",
            "RESIDENT_REMOTE_RETURNED": "return_remote",
            "STOCK_ASSET_ISSUED": "issue_remote",
            "DIGITAL_ACCESS_ACTIVATED": "activate_phone",
        }.get(code)
        if action_key:
            rows.append([actions[action_key]])
    rows.extend([["⬅️ К оператору"], [HOME]])
    return rows


async def _show_operator_order_card(
    update: Update,
    state: dict,
    user_id: int,
    order_id: int,
    lang: str,
) -> None:
    order = service_order_summary(order_id)
    try:
        _assert_operator_order_access(user_id, order)
    except Exception:
        await update.message.reply_text(tr(lang, "denied"))
        return
    state["mode"] = "operator_order_card"
    state["order_id"] = int(order_id)
    await update.message.reply_text(
        _order_card(order, lang=lang, title="🔑 Заявка оператора"),
        reply_markup=kb(_operator_order_actions(order, lang)),
    )


def _stock_assets_for(order: dict) -> list[dict]:
    profile = text(order.get("workflow_profile_code"))
    wanted = "NEW" if profile == "REMOTE_NEW_FROM_STOCK" else "REFURBISHED"
    conn = get_conn()
    try:
        cur = conn.cursor()
        if wanted == "NEW":
            cur.execute(
                """
                SELECT *
                FROM remote_assets
                WHERE inventory_status = 'AVAILABLE'
                  AND condition_status IN ('NEW', 'UNKNOWN')
                  AND ownership_type IN ('OSBB_STOCK', 'OSBB')
                ORDER BY asset_number, id
                LIMIT 40
                """
            )
        else:
            cur.execute(
                """
                SELECT *
                FROM remote_assets
                WHERE inventory_status = 'AVAILABLE'
                  AND condition_status IN ('REFURBISHED', 'REFURB', 'USED_READY')
                  AND ownership_type IN ('OSBB_STOCK', 'OSBB')
                ORDER BY asset_number, id
                LIMIT 40
                """
            )
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def _payments_columns(cur: sqlite3.Cursor) -> set[str]:
    """
    Return actual columns of the payments table.

    The older OSBB cashier schema stores apartment_number, while the service
    schema may use apartment_id.  The service workspace must work with both
    during the migration period.
    """
    cur.execute("PRAGMA table_info(payments)")
    return {str(row[1]) for row in cur.fetchall()}


def _matching_payments(order: dict) -> tuple[list[dict], float, float]:
    """
    Return unlinked confirmed payments matching the order.

    Compatibility rules:
    - newer payment schemas may contain apartment_id and source_ref;
    - older schemas contain apartment_number and do not have source_ref.
    The returned row always has a source_ref key, set to None when the
    database does not yet have that column.
    """
    due = float(order.get("amount_due_snapshot") or 0)
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM service_order_payment_links
            WHERE service_order_id = ?
            """,
            (int(order["id"]),),
        )
        linked = float(cur.fetchone()[0] or 0)
        remaining = max(0.0, due - linked)

        columns = _payments_columns(cur)

        if "apartment_id" in columns:
            apartment_where = "p.apartment_id = ?"
            apartment_value: Any = int(order["apartment_id"])
        elif "apartment_number" in columns:
            apartment_where = "CAST(p.apartment_number AS TEXT) = ?"
            apartment_value = text(order.get("apartment_number"))
        else:
            raise RuntimeError(
                "В таблице payments нет ни apartment_id, ни apartment_number. "
                "Невозможно безопасно подобрать оплату к заявке."
            )

        source_ref_select = (
            "p.source_ref AS source_ref"
            if "source_ref" in columns
            else "NULL AS source_ref"
        )

        if "service_item_code" in columns:
            service_where = "AND COALESCE(p.service_item_code, '') = COALESCE(?, '')"
            service_params: tuple[Any, ...] = (order.get("service_item_code"),)
        else:
            # Do not ever offer a payment from another service if the source
            # schema cannot identify the service item.
            service_where = "AND 1 = 0"
            service_params = ()

        cashier_where = (
            "AND COALESCE(p.cashier_entry_status, 'CONFIRMED') = 'CONFIRMED'"
            if "cashier_entry_status" in columns
            else ""
        )

        cur.execute(
            f"""
            SELECT
                p.id, p.payment_date, p.amount, p.currency,
                p.payment_method, p.payment_channel,
                {source_ref_select}, p.cashbox_code, p.comment
            FROM payments p
            LEFT JOIN service_order_payment_links l
              ON l.payment_id = p.id
            WHERE l.id IS NULL
              AND {apartment_where}
              {service_where}
              {cashier_where}
              AND COALESCE(p.amount, 0) > 0
            ORDER BY p.id ASC
            LIMIT 40
            """,
            (apartment_value, *service_params),
        )
        return [dict(row) for row in cur.fetchall()], linked, remaining
    finally:
        conn.close()

def _write_ui_audit(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    action_type: str,
    category: str,
    order_id: int,
    details: str,
) -> None:
    write_access_audit(
        conn,
        actor_user_id=user_id,
        action_type=action_type,
        resource="service_orders",
        action="CONFIRM",
        scope_type="SERVICE_CATEGORY",
        scope_value=category,
        target_table="service_orders",
        target_id=order_id,
        details=details,
    )


def _receive_resident_remote(order: dict, asset_number: str, user_id: int) -> dict:
    category = _assert_operator_order_access(user_id, order, "CREATE")
    conn = get_conn()
    try:
        asset = create_remote_asset(
            asset_number=text(asset_number),
            ownership_type="RESIDENT",
            inventory_status="IN_SERVICE",
            condition_status="UNKNOWN",
            apartment_id=int(order["apartment_id"]),
            apartment_number=text(order.get("apartment_number")),
            actor_id=user_id,
            note=f"Принят по заявке {order['order_number']}.",
            conn=conn,
        )
        result = record_remote_movement(
            remote_asset_id=int(asset["id"]),
            service_order_id=int(order["id"]),
            movement_type="RECEIVED_FROM_RESIDENT",
            to_state="IN_SERVICE",
            actor_id=user_id,
            apartment_id=int(order["apartment_id"]),
            apartment_number=text(order.get("apartment_number")),
            note="Пульт жильца принят на пост O.",
            confirm_step_code="RESIDENT_REMOTE_RECEIVED",
            conn=conn,
        )
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE remote_order_details
            SET resident_asset_id = ?, updated_at = ?
            WHERE service_order_id = ?
            """,
            (int(asset["id"]), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(order["id"])),
        )
        _write_ui_audit(
            conn, user_id=user_id, action_type="resident_remote_received",
            category=category, order_id=int(order["id"]),
            details=f"asset={asset['asset_number']}",
        )
        conn.commit()
        return result["order"]
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _reserve_stock_remote(order: dict, asset_id: int, user_id: int) -> dict:
    category = _assert_operator_order_access(user_id, order, "CREATE")
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM remote_assets WHERE id = ?", (int(asset_id),))
        row = cur.fetchone()
        if not row:
            raise ValueError("Пульт не найден.")
        asset = dict(row)
        if text(asset.get("inventory_status")) != "AVAILABLE":
            raise ValueError("Этот пульт уже недоступен для резерва.")
        result = record_remote_movement(
            remote_asset_id=int(asset_id),
            service_order_id=int(order["id"]),
            movement_type="RESERVED_FOR_ORDER",
            to_state="RESERVED",
            actor_id=user_id,
            apartment_id=int(order["apartment_id"]),
            apartment_number=text(order.get("apartment_number")),
            note=f"Резерв для заявки {order['order_number']}.",
            confirm_step_code="STOCK_ASSET_RESERVED",
            conn=conn,
        )
        cur.execute(
            """
            UPDATE remote_order_details
            SET issued_asset_id = ?, updated_at = ?
            WHERE service_order_id = ?
            """,
            (int(asset_id), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(order["id"])),
        )
        _write_ui_audit(
            conn, user_id=user_id, action_type="stock_remote_reserved",
            category=category, order_id=int(order["id"]),
            details=f"asset={asset.get('asset_number')}",
        )
        conn.commit()
        return result["order"]
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _program_remote(order: dict, user_id: int) -> dict:
    _assert_operator_order_access(user_id, order, "CONFIRM")
    from service_orders_core import confirm_order_step
    return confirm_order_step(
        order_id=int(order["id"]),
        step_code="REMOTE_PROGRAMMED",
        actor_id=user_id,
        note="Перепрошивка подтверждена оператором.",
        source_context="service_orders_workspace",
    )


def _return_or_issue_remote(order: dict, user_id: int, *, issue_from_stock: bool) -> dict:
    category = _assert_operator_order_access(user_id, order, "CONFIRM")
    details = _order_remote_details(int(order["id"]))
    field = "issued_asset_id" if issue_from_stock else "resident_asset_id"
    asset_id = details.get(field)
    if not asset_id:
        raise ValueError("Для заявки не указан конкретный физический пульт.")
    conn = get_conn()
    try:
        result = record_remote_movement(
            remote_asset_id=int(asset_id),
            service_order_id=int(order["id"]),
            movement_type="ISSUED_TO_RESIDENT" if issue_from_stock else "RETURNED_TO_RESIDENT",
            to_state="WITH_RESIDENT",
            actor_id=user_id,
            apartment_id=int(order["apartment_id"]),
            apartment_number=text(order.get("apartment_number")),
            note=(
                "Новый/восстановленный пульт выдан жильцу."
                if issue_from_stock else "Собственный пульт возвращён жильцу."
            ),
            confirm_step_code="STOCK_ASSET_ISSUED" if issue_from_stock else "RESIDENT_REMOTE_RETURNED",
            conn=conn,
        )
        cur = conn.cursor()
        if issue_from_stock:
            cur.execute(
                """
                UPDATE remote_assets
                SET ownership_type = 'RESIDENT',
                    issued_at = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    int(asset_id),
                ),
            )
        _write_ui_audit(
            conn, user_id=user_id,
            action_type="stock_remote_issued" if issue_from_stock else "resident_remote_returned",
            category=category, order_id=int(order["id"]),
            details=f"asset_id={asset_id}",
        )
        conn.commit()
        return result["order"]
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _activate_phone(order: dict, phone: str, user_id: int) -> dict:
    _assert_operator_order_access(user_id, order, "CONFIRM")
    return activate_access_credential(
        order_id=int(order["id"]),
        credential_value=phone,
        actor_id=user_id,
        apartment_id=int(order["apartment_id"]),
        apartment_number=text(order.get("apartment_number")),
        external_reference="",
        note="Телефонный доступ активирован оператором.",
    )["order"]


def _inventory_text() -> str:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT condition_status, COUNT(*) AS qty
            FROM remote_assets
            WHERE inventory_status = 'AVAILABLE'
              AND ownership_type IN ('OSBB_STOCK', 'OSBB')
            GROUP BY condition_status
            ORDER BY condition_status
            """
        )
        rows = cur.fetchall()
        lines = ["📦 Доступный остаток пультов", ""]
        if not rows:
            lines.append("Нет доступных пультов.")
        else:
            for row in rows:
                lines.append(f"{row['condition_status'] or 'UNKNOWN'}: {row['qty']} шт.")
        return "\n".join(lines)
    finally:
        conn.close()


async def _handle_operator(
    update: Update,
    user_states: dict,
    user_id: int,
    message_text: str,
    *,
    lang: str,
    state: dict,
) -> bool:
    if _home_text(message_text):
        user_states.pop(user_id, None)
        return False

    if not has_service_workspace_access(user_id):
        await update.message.reply_text(tr(lang, "denied"))
        return True

    mode = text(state.get("mode"))
    if _operator_back_text(message_text):
        await show_service_operator_workspace(update, user_states, user_id, lang=lang)
        return True

    if mode == "operator_home":
        if message_text in {tr(lang, "open_orders"), tr(lang, "refresh")}:
            await _show_operator_orders(update, state, user_id, lang)
            return True
        if message_text == tr(lang, "inventory"):
            await update.message.reply_text(
                _inventory_text(),
                reply_markup=kb([["⬅️ К оператору"], [HOME]]),
            )
            return True
        await update.message.reply_text(tr(lang, "wrong"))
        return True

    if mode == "operator_orders":
        order_id = (state.get("operator_order_buttons") or {}).get(message_text)
        if order_id:
            await _show_operator_order_card(update, state, user_id, int(order_id), lang)
            return True
        await update.message.reply_text(tr(lang, "wrong"))
        return True

    if mode == "operator_order_card":
        order = service_order_summary(int(state["order_id"]))
        action_by_text = {value: key for key, value in _operator_action_texts(lang).items()}
        action = action_by_text.get(message_text)
        if not action:
            await update.message.reply_text(tr(lang, "wrong"))
            return True

        try:
            _assert_operator_order_access(user_id, order)
        except Exception:
            await update.message.reply_text(tr(lang, "denied"))
            return True

        if action == "receive_remote":
            state["mode"] = "operator_receive_remote_label"
            await update.message.reply_text(
                tr(lang, "asset_prompt"),
                reply_markup=kb([["⬅️ К оператору"], [HOME]]),
            )
            return True

        if action == "reserve_remote":
            rows = _stock_assets_for(order)
            if not rows:
                await update.message.reply_text(
                    tr(lang, "no_stock"),
                    reply_markup=kb(_operator_order_actions(order, lang)),
                )
                return True
            mapping: dict[str, int] = {}
            buttons: list[list[str]] = []
            for asset in rows:
                label = f"📦 {asset.get('asset_number')} | {asset.get('condition_status')}"
                mapping[label] = int(asset["id"])
                buttons.append([label])
            state["stock_asset_buttons"] = mapping
            state["mode"] = "operator_reserve_select"
            await update.message.reply_text(
                tr(lang, "choose_stock"),
                reply_markup=kb(buttons + [["⬅️ К оператору"], [HOME]]),
            )
            return True

        if action == "link_payment":
            rows, linked, remaining = _matching_payments(order)
            if not rows:
                await update.message.reply_text(
                    tr(lang, "no_payments"),
                    reply_markup=kb(_operator_order_actions(order, lang)),
                )
                return True
            mapping: dict[str, dict] = {}
            buttons: list[list[str]] = []
            for payment in rows:
                label = (
                    f"💳 #{payment['id']} | {money(payment.get('amount'))} | "
                    f"{payment.get('payment_method') or '-'} | "
                    f"{payment.get('source_ref') or payment.get('cashbox_code') or '-'}"
                )
                mapping[label] = payment
                buttons.append([label])
            state["payment_buttons"] = mapping
            state["payment_remaining"] = remaining
            state["mode"] = "operator_payment_select"
            await update.message.reply_text(
                f"{tr(lang, 'choose_payment')}\n"
                f"К оплате: {money(order.get('amount_due_snapshot'))}; "
                f"уже привязано: {money(linked)}; остаток: {money(remaining)}.",
                reply_markup=kb(buttons + [["⬅️ К оператору"], [HOME]]),
            )
            return True

        try:
            if action == "program_done":
                _program_remote(order, user_id)
            elif action == "return_remote":
                _return_or_issue_remote(order, user_id, issue_from_stock=False)
            elif action == "issue_remote":
                _return_or_issue_remote(order, user_id, issue_from_stock=True)
            elif action == "activate_phone":
                state["mode"] = "operator_phone_input"
                await update.message.reply_text(
                    tr(lang, "phone_prompt"),
                    reply_markup=kb([["⬅️ К оператору"], [HOME]]),
                )
                return True
            else:
                raise ValueError("Неизвестное действие.")
        except Exception as exc:
            await update.message.reply_text(f"⚠️ {exc}")
            return True
        await _show_operator_order_card(update, state, user_id, int(order["id"]), lang)
        return True

    if mode == "operator_receive_remote_label":
        if _operator_back_text(message_text):
            await _show_operator_order_card(update, state, user_id, int(state["order_id"]), lang)
            return True
        if len(text(message_text)) < 3:
            await update.message.reply_text("Маркировка должна содержать минимум 3 символа.")
            return True
        order = service_order_summary(int(state["order_id"]))
        try:
            _receive_resident_remote(order, text(message_text), user_id)
        except Exception as exc:
            await update.message.reply_text(f"⚠️ {exc}")
            return True
        await _show_operator_order_card(update, state, user_id, int(order["id"]), lang)
        return True

    if mode == "operator_reserve_select":
        asset_id = (state.get("stock_asset_buttons") or {}).get(message_text)
        if not asset_id:
            await update.message.reply_text(tr(lang, "wrong"))
            return True
        order = service_order_summary(int(state["order_id"]))
        try:
            _reserve_stock_remote(order, int(asset_id), user_id)
        except Exception as exc:
            await update.message.reply_text(f"⚠️ {exc}")
            return True
        await _show_operator_order_card(update, state, user_id, int(order["id"]), lang)
        return True

    if mode == "operator_payment_select":
        payment = (state.get("payment_buttons") or {}).get(message_text)
        if not payment:
            await update.message.reply_text(tr(lang, "wrong"))
            return True
        order = service_order_summary(int(state["order_id"]))
        remaining = float(state.get("payment_remaining") or 0)
        amount = min(float(payment.get("amount") or 0), remaining)
        if amount <= 0:
            await update.message.reply_text("Для привязки не осталось суммы.")
            return True
        try:
            link_payment_to_order(
                order_id=int(order["id"]),
                payment_id=int(payment["id"]),
                amount=amount,
                actor_id=user_id,
                note=f"Привязано оператором к {order['order_number']}.",
            )
        except Exception as exc:
            await update.message.reply_text(f"⚠️ {exc}")
            return True
        await _show_operator_order_card(update, state, user_id, int(order["id"]), lang)
        return True

    if mode == "operator_phone_input":
        if _operator_back_text(message_text):
            await _show_operator_order_card(update, state, user_id, int(state["order_id"]), lang)
            return True
        phone = re.sub(r"[\s()\-]", "", text(message_text))
        if not re.fullmatch(r"\+?\d{8,20}", phone):
            await update.message.reply_text(tr(lang, "wrong_phone"))
            return True
        order = service_order_summary(int(state["order_id"]))
        try:
            _activate_phone(order, phone, user_id)
        except Exception as exc:
            await update.message.reply_text(f"⚠️ {exc}")
            return True
        await _show_operator_order_card(update, state, user_id, int(order["id"]), lang)
        return True

    await show_service_operator_workspace(update, user_states, user_id, lang=lang)
    return True


async def handle_service_orders_text(
    update: Update,
    user_states: dict,
    user_id: int,
    message_text: str,
    *,
    lang: str,
    user_mode: str | None,
) -> bool:
    """
    Called by parking_bot before the generic client portal parser.

    It does not grant permissions itself: each operator-side core operation
    re-checks the relevant role/action/scope on the server.
    """
    message_text = text(message_text)
    lang = lang if lang in I18N else "ru"

    if message_text in _operator_mode_texts():
        await show_service_operator_workspace(update, user_states, user_id, lang=lang)
        return True

    state = _state(user_states, user_id, create=False)
    if state:
        area = text(state.get("area"))
        if area == "resident":
            return await _handle_resident(
                update, user_states, user_id, message_text, lang=lang, state=state
            )
        if area == "operator":
            return await _handle_operator(
                update, user_states, user_id, message_text, lang=lang, state=state
            )

    if user_mode == "client" and message_text in _resident_entry_texts():
        await show_resident_services(update, user_states, user_id, lang=lang)
        return True

    if (
        user_mode == "admin"
        and message_text in {"🔑 Заявки на пульты", "📞 Телефонный доступ"}
        and has_service_workspace_access(user_id)
    ):
        await show_service_operator_workspace(update, user_states, user_id, lang=lang)
        return True

    return False
