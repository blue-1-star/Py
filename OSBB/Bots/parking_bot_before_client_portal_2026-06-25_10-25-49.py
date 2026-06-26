from pathlib import Path
import sys

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
# from Bots.handlers.vehicle_verification import handle_vehicle_verification_text
from handlers.vehicle_verification import handle_vehicle_verification_text
from handlers.vehicle_card_editor import handle_vehicle_card_editor_text
from handlers.vehicle_full_list import handle_vehicle_full_list_text
from handlers.audit_viewer import handle_audit_viewer_text
from handlers.unit_registry_editor import handle_unit_registry_editor_text
BOT_DIR = Path(__file__).resolve().parent
OSBB_ROOT = BOT_DIR.parent
PY_ROOT = OSBB_ROOT.parent

for p in (OSBB_ROOT, PY_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from config import paths

if str(paths.SECRETS_DIR) not in sys.path:
    sys.path.insert(0, str(paths.SECRETS_DIR))

from telegram_osbb import (
    TOKEN,
    SUPER_ADMIN_IDS,
    ADMIN_IDS,
)

from Bots.db_access import (
    upsert_resident_account_from_telegram,
    get_resident_account,
    link_resident_to_apartment,
    get_apartment_vehicles,
    format_vehicle_list,
    find_apartment,
    get_resident_accounts_summary,
    format_resident_accounts_summary,
    get_resident_accounts_by_filter,
    format_resident_accounts_list,
    get_resident_account_by_telegram_id,
    format_resident_account_card,
    mark_resident_operator_verified,
    unlink_resident_account,
    get_next_vehicle_for_review,
    set_vehicle_day,
    set_vehicle_night,
    set_vehicle_inactive,
    skip_vehicle_review,
    get_vehicle_review_stats,
    format_vehicle_review_card,
    get_vehicles_by_status,
    format_vehicles_admin_list,
    get_apartment_card,
    format_apartment_card,
    get_vehicle_by_id_for_apartment,
    format_vehicle_card_for_edit,
    update_vehicle_parking_status,
    update_vehicle_plate,
    update_vehicle_model,
)


from Bots.handlers.agreement import (
    AGREEMENT_MENU,
    AGREEMENT_ACTION_MENU,
    show_agreement_menu,
    show_next_agreement_apartment,
    show_agreement_list,
    show_agreement_stats,
    handle_waiting_agreement_apartment,
    handle_agreement_card_action,
    handle_agreement_menu_text,
)

user_languages = {}
user_modes = {}
user_states = {}
user_admin_apartments = {}
user_admin_vehicles = {}


TEXTS = {
    "ru": {
        "choose_language": "Оберіть мову / Выберите язык / Choose language",
        "mode": "Выберите режим:",
        "client_mode": "👤 Клиентский режим",
        "admin_mode": "🔐 Админ-режим",
        "welcome": "Добро пожаловать в систему управления ОСББ.",
        "parking": "🚗 Парковка",
        "remotes": "🔑 Пульты",
        "improvement": "🏗 Благоустройство",
        "news": "📢 Объявления",
        "contacts": "📞 Контакты",
    },
    "uk": {
        "choose_language": "Оберіть мову / Выберите язык / Choose language",
        "mode": "Оберіть режим:",
        "client_mode": "👤 Режим мешканця",
        "admin_mode": "🔐 Адмін-режим",
        "welcome": "Ласкаво просимо до системи ОСББ.",
        "parking": "🚗 Паркування",
        "remotes": "🔑 Пульти",
        "improvement": "🏗 Благоустрій",
        "news": "📢 Оголошення",
        "contacts": "📞 Контакти",
    },
    "en": {
        "choose_language": "Оберіть мову / Выберите язык / Choose language",
        "mode": "Choose mode:",
        "client_mode": "👤 User mode",
        "admin_mode": "🔐 Admin mode",
        "welcome": "Welcome to the OSBB management system.",
        "parking": "🚗 Parking",
        "remotes": "🔑 Remotes",
        "improvement": "🏗 Improvements",
        "news": "📢 Announcements",
        "contacts": "📞 Contacts",
    },
}


LANG_MENU = [
    ["🇺🇦 Українська"],
    ["🇷🇺 Русский"],
    ["🇬🇧 English"],
]

CLIENT_MENU_RU = [
    ["🏠 Моя квартира"],
    ["✏️ Изменить квартиру"],
    ["🚗 Мои автомобили"],
    ["🚗 Парковка", "🔑 Пульты"],
    ["📞 Открытие по телефону"],
    ["🏗 Благоустройство"],
    ["📢 Объявления", "📞 Контакты"],
    ["🔐 Админ-режим"],
]

ADMIN_MENU = [
    ["🏠 Квартиры", "🏢 Помещения"],
    ["👥 Пользователи"],
    ["🚗 Автомобили"],
    ["🚗 Проверка авто"],
    ["🧾 Журнал действий"],
    ["🤝 Согласование"],
    ["🔑 Заявки на пульты"],
    ["📞 Телефонный доступ"],
    ["💳 Платежи"],
    ["📊 Отчёты"],
    ["⚙️ Настройки"],
    ["👤 Клиентский режим"],
]

USERS_MENU = [
    ["📋 Все пользователи"],
    ["🏠 Без квартиры"],
    ["⏳ Самоподтверждённые"],
    ["✅ Проверенные оператором"],
    ["🔎 Проверить пользователя"],
    ["❌ Отвязать квартиру"],
    ["⬅️ Назад"],
]
APARTMENT_MENU = [
    ["👥 Жильцы", "🚗 Авто"],
    ["💳 Платежи", "📞 Телефоны"],
    ["🔑 Пульты"],
    ["🏠 Квартиры"],
    ["⬅️ Назад"],
]

CONFIRM_APARTMENT_MENU = [
    ["✅ Да, это моя квартира"],
    ["✏️ Ввести другую квартиру"],
    ["🏠 Главное меню"],
]

USER_VERIFY_MENU = [
    ["✅ Подтвердить пользователя"],
    ["❌ Отвязать квартиру"],
    ["👥 Пользователи"],
    ["⬅️ Назад"],
]
VEHICLE_REVIEW_MENU = [
    ["📋 Все автомобили"],
    ["🔎 Найти авто"],
    ["❓ Без статуса"],
    ["☀️ Day", "🌙 Night"],
    ["🚫 Не паркуется"],
    ["📊 Статистика авто"],
    ["⬅️ Назад"],
]

VEHICLE_ACTION_MENU = [
    ["☀️ Day"],
    ["🌙 Night"],
    ["🚫 Не паркуется"],
    ["⏭ Пропустить"],
    ["⛔ Завершить"],
]

VEHICLE_EDIT_MENU = [
    ["✏️ Статус"],
    ["✏️ Номер", "✏️ Марка"],
    ["🏠 Перенести"],
    ["⬅️ Назад"],
]

VEHICLE_STATUS_MENU = [
    ["☀️ Day", "🌙 Night"],
    ["🚫 Не паркуется", "❓ NULL"],
    ["⬅️ Назад"],
]

def kb(buttons):
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def is_admin_user(user_id: int) -> bool:
    return user_id in ADMIN_IDS or user_id in SUPER_ADMIN_IDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    upsert_resident_account_from_telegram(user)

    await update.message.reply_text(
        TEXTS["ru"]["choose_language"],
        reply_markup=kb(LANG_MENU),
    )


async def show_mode_menu(update: Update, lang: str):
    t = TEXTS[lang]
    await update.message.reply_text(
        t["mode"],
        reply_markup=kb([[t["client_mode"]], [t["admin_mode"]]]),
    )


async def show_client_menu(update: Update, lang: str):
    t = TEXTS[lang]
    await update.message.reply_text(
        t["welcome"],
        reply_markup=kb(CLIENT_MENU_RU),
    )


async def show_admin_menu(update: Update):
    await update.message.reply_text(
        "🔐 Админ-режим\n\nВыберите раздел:",
        reply_markup=kb(ADMIN_MENU),
    )


async def show_users_menu(update: Update):
    summary = get_resident_accounts_summary(limit=10)

    await update.message.reply_text(
        format_resident_accounts_summary(summary) + "\n\nВыберите список:",
        reply_markup=kb(USERS_MENU),
    )


async def show_resident_list(update: Update, title: str, filter_name: str):
    rows = get_resident_accounts_by_filter(filter_name, limit=30)

    await update.message.reply_text(
        format_resident_accounts_list(title, rows),
        reply_markup=kb(USERS_MENU),
    )


async def show_my_apartment(update: Update, user_id: int):
    account = get_resident_account(user_id)

    if not account or not account[6]:
        user_states[user_id] = "waiting_apartment"
        await update.message.reply_text("Введите номер квартиры:")
        return

    apartment_number = account[6]

    await update.message.reply_text(
        f"🏠 Ваша квартира: {apartment_number}",
        reply_markup=kb(CLIENT_MENU_RU),
    )


async def show_my_vehicles(update: Update, user_id: int):
    account = get_resident_account(user_id)

    if not account or not account[6]:
        user_states[user_id] = "waiting_apartment"
        await update.message.reply_text(
            "Сначала нужно привязать квартиру.\n\n"
            "Введите номер квартиры:"
        )
        return

    apartment_number = account[6]
    vehicles = get_apartment_vehicles(apartment_number)

    await update.message.reply_text(
        f"🚗 Автомобили квартиры {apartment_number}\n\n"
        f"{format_vehicle_list(vehicles)}",
        reply_markup=kb(CLIENT_MENU_RU),
    )


async def handle_waiting_apartment(update: Update, user_id: int, text: str):
    apartment_number = text.strip()
    apt = find_apartment(apartment_number)

    if not apt:
        await update.message.reply_text(
            "Квартира не найдена в базе.\n\n"
            "Проверьте номер и введите ещё раз:"
        )
        return

    vehicles = get_apartment_vehicles(apartment_number)

    user_states[user_id] = ("confirm_apartment", apartment_number)

    await update.message.reply_text(
        f"Квартира {apartment_number}\n\n"
        f"Автомобили в базе:\n"
        f"{format_vehicle_list(vehicles)}\n\n"
        f"Это ваша квартира?",
        reply_markup=kb(CONFIRM_APARTMENT_MENU),
    )


async def handle_confirm_apartment(update: Update, user_id: int, text: str, lang: str):
    state = user_states.get(user_id)

    if text == "✏️ Ввести другую квартиру":
        user_states[user_id] = "waiting_apartment"
        await update.message.reply_text("Введите номер квартиры:")
        return

    if text == "🏠 Главное меню":
        user_states.pop(user_id, None)
        await show_client_menu(update, lang)
        return

    if text not in ["✅ Да, это моя квартира", "ДА", "Да", "да"]:
        await update.message.reply_text(
            "Пожалуйста, выберите кнопку.",
            reply_markup=kb(CONFIRM_APARTMENT_MENU),
        )
        return

    if not (isinstance(state, tuple) and state[0] == "confirm_apartment"):
        user_states.pop(user_id, None)
        await show_client_menu(update, lang)
        return

    apartment_number = state[1]

    ok, msg = link_resident_to_apartment(user_id, apartment_number)

    if ok:
        user_states.pop(user_id, None)
        await update.message.reply_text(
            f"Квартира {apartment_number} привязана.\n\n"
            f"Теперь можно пользоваться меню.",
            reply_markup=kb(CLIENT_MENU_RU),
        )
    else:
        await update.message.reply_text(f"Ошибка привязки квартиры: {msg}")


async def ask_user_to_verify(update: Update):
    user_states[update.effective_user.id] = "admin_waiting_user_id_verify"
    await update.message.reply_text(
        "Введите Telegram ID пользователя для проверки.\n\n"
        "ID видно в списке пользователей первой колонкой, если он включён в вывод.",
        reply_markup=kb([["👥 Пользователи"], ["⬅️ Назад"]]),
    )


async def ask_user_to_unlink(update: Update):
    user_states[update.effective_user.id] = "admin_waiting_user_id_unlink"
    await update.message.reply_text(
        "Введите Telegram ID пользователя, которому нужно отвязать квартиру.",
        reply_markup=kb([["👥 Пользователи"], ["⬅️ Назад"]]),
    )


async def handle_admin_waiting_user_id(update: Update, user_id: int, text: str, action: str):
    if text in ["👥 Пользователи", "⬅️ Назад"]:
        user_states.pop(user_id, None)
        await show_users_menu(update)
        return

    try:
        target_user_id = int(text.strip())
    except ValueError:
        await update.message.reply_text(
            "Нужно ввести числовой Telegram ID пользователя."
        )
        return

    account = get_resident_account_by_telegram_id(target_user_id)

    if not account:
        await update.message.reply_text(
            "Пользователь не найден в resident_accounts."
        )
        return

    if action == "verify":
        user_states[user_id] = ("admin_confirm_verify_user", target_user_id)
        await update.message.reply_text(
            format_resident_account_card(account)
            + "\n\nПодтвердить этого пользователя оператором?",
            reply_markup=kb(USER_VERIFY_MENU),
        )
        return

    if action == "unlink":
        user_states[user_id] = ("admin_confirm_unlink_user", target_user_id)
        await update.message.reply_text(
            format_resident_account_card(account)
            + "\n\nОтвязать квартиру у этого пользователя?",
            reply_markup=kb(USER_VERIFY_MENU),
        )
        return


async def handle_admin_confirm_user_action(update: Update, user_id: int, text: str):
    state = user_states.get(user_id)

    if text in ["👥 Пользователи", "⬅️ Назад"]:
        user_states.pop(user_id, None)
        await show_users_menu(update)
        return

    if not isinstance(state, tuple):
        user_states.pop(user_id, None)
        await show_users_menu(update)
        return

    action = state[0]
    target_user_id = state[1]

    if action == "admin_confirm_verify_user":
        if text != "✅ Подтвердить пользователя":
            await update.message.reply_text(
                "Выберите действие.",
                reply_markup=kb(USER_VERIFY_MENU),
            )
            return

        ok, msg = mark_resident_operator_verified(target_user_id)

        user_states.pop(user_id, None)

        await update.message.reply_text(
            "Пользователь подтверждён оператором." if ok else f"Ошибка: {msg}",
            reply_markup=kb(USERS_MENU),
        )
        return

    if action == "admin_confirm_unlink_user":
        if text != "❌ Отвязать квартиру":
            await update.message.reply_text(
                "Выберите действие.",
                reply_markup=kb(USER_VERIFY_MENU),
            )
            return

        ok, msg = unlink_resident_account(target_user_id)

        user_states.pop(user_id, None)

        await update.message.reply_text(
            "Квартира отвязана от пользователя." if ok else f"Ошибка: {msg}",
            reply_markup=kb(USERS_MENU),
        )
        return

async def show_apartment_card(update: Update, user_id: int, apartment_number: str):
    card = get_apartment_card(apartment_number)

    if not card:
        await update.message.reply_text(
            "Квартира не найдена.",
            reply_markup=kb(ADMIN_MENU),
        )
        return

    user_admin_apartments[user_id] = str(apartment_number)

    await update.message.reply_text(
        format_apartment_card(card),
        reply_markup=kb(APARTMENT_MENU),
    )


def build_number_keyboard(count: int, back_text="⬅️ Назад"):
    rows = []
    row = []

    for i in range(1, count + 1):
        row.append(str(i))

        if len(row) == 3:
            rows.append(row)
            row = []

    if row:
        rows.append(row)

    rows.append([back_text])
    return rows


async def show_current_apartment_vehicles(update: Update, user_id: int):
    apartment_number = user_admin_apartments.get(user_id)

    if not apartment_number:
        user_states[user_id] = "admin_waiting_apartment_lookup"
        await update.message.reply_text(
            "Сначала выберите квартиру:",
            reply_markup=kb([["⬅️ Назад"]]),
        )
        return

    vehicles = get_apartment_vehicles(apartment_number)
    user_admin_vehicles[user_id] = vehicles

    lines = []
    for idx, row in enumerate(vehicles, start=1):
        plate = row[1] or row[2] or "-"
        model = row[3] or row[4] or "-"
        status = row[5] or "NULL"
        lines.append(f"{idx}. {plate} | {model} | {status}")

    user_states[user_id] = ("vehicle_select_in_apartment", apartment_number)

    await update.message.reply_text(
        f"🚗 Авто кв.{apartment_number}\n\n"
        f"{chr(10).join(lines) if lines else 'нет авто'}\n\n"
        "Выберите строку:",
        reply_markup=kb(build_number_keyboard(len(vehicles))),
    )


async def show_current_apartment_residents(update: Update, user_id: int):
    apartment_number = user_admin_apartments.get(user_id)

    if not apartment_number:
        user_states[user_id] = "admin_waiting_apartment_lookup"
        await update.message.reply_text(
            "Сначала выберите квартиру:",
            reply_markup=kb([["⬅️ Назад"]]),
        )
        return

    card = get_apartment_card(apartment_number)

    if not card:
        await update.message.reply_text(
            "Квартира не найдена.",
            reply_markup=kb(ADMIN_MENU),
        )
        return

    lines = [f"👥 Жильцы кв.{apartment_number}", ""]

    if card["residents"]:
        for first_name, last_name, username, status in card["residents"]:
            name = " ".join(x for x in [first_name, last_name] if x) or "-"
            username = f"@{username}" if username else "-"
            status = status or "-"
            lines.append(f"• {name} | {username} | {status}")
    else:
        lines.append("нет пользователей")

    await update.message.reply_text(
        "\n".join(lines),
        reply_markup=kb(APARTMENT_MENU),
    )


async def show_vehicle_card(update: Update, user_id: int, vehicle_id: int):
    apartment_number = user_admin_apartments.get(user_id)
    vehicle = get_vehicle_by_id_for_apartment(vehicle_id, apartment_number)

    if not vehicle:
        await update.message.reply_text(
            "Автомобиль не найден.",
            reply_markup=kb(APARTMENT_MENU),
        )
        return

    user_states[user_id] = ("vehicle_card", vehicle_id)

    await update.message.reply_text(
        format_vehicle_card_for_edit(vehicle) + "\n\nВыберите действие:",
        reply_markup=kb(VEHICLE_EDIT_MENU),
    )


async def show_vehicle_menu(update: Update):
    await update.message.reply_text(
        "🚗 Автомобили\n\n"
        "Выберите действие:",
        reply_markup=kb(VEHICLE_REVIEW_MENU),
    )


async def show_vehicle_stats(update: Update):
    stats = get_vehicle_review_stats()

    total = stats["total"]
    day_count = stats["Day"]
    night_count = stats["Night"]
    inactive_count = stats["Inactive"]
    missing_count = stats["missing"]

    filled = day_count + night_count + inactive_count
    percent = round((filled / total) * 100, 1) if total else 0

    await update.message.reply_text(
        "📊 Статистика автомобилей\n\n"
        f"Всего авто: {total}\n"
        f"☀️ Day: {day_count}\n"
        f"🌙 Night: {night_count}\n"
        f"🚫 Не паркуется: {inactive_count}\n"
        f"❓ Без тарифа/статуса: {missing_count}\n\n"
        f"Заполнено: {filled} из {total} ({percent}%)",
        reply_markup=kb(VEHICLE_REVIEW_MENU),
    )


async def show_next_vehicle_for_review(update: Update, user_id: int):
    vehicle = get_next_vehicle_for_review()

    if not vehicle:
        user_states.pop(user_id, None)

        await update.message.reply_text(
            "✅ Все автомобили уже имеют статус Day / Night / Не паркуется.",
            reply_markup=kb(VEHICLE_REVIEW_MENU),
        )
        return

    vehicle_id = vehicle[0]
    user_states[user_id] = ("vehicle_review", vehicle_id)

    await update.message.reply_text(
        format_vehicle_review_card(vehicle),
        reply_markup=kb(VEHICLE_ACTION_MENU),
    )


async def handle_vehicle_review_action(update: Update, user_id: int, text: str):
    state = user_states.get(user_id)

    if not (isinstance(state, tuple) and state[0] == "vehicle_review"):
        user_states.pop(user_id, None)
        await show_vehicle_menu(update)
        return

    vehicle_id = state[1]

    if text == "⛔ Завершить":
        user_states.pop(user_id, None)

        await update.message.reply_text(
            "Проверка автомобилей завершена.",
            reply_markup=kb(VEHICLE_REVIEW_MENU),
        )
        return

    if text == "⏭ Пропустить":
        skip_vehicle_review(vehicle_id)
        await update.message.reply_text("⏭ Пропущено.")
        await show_next_vehicle_for_review(update, user_id)
        return

    if text == "☀️ Day":
        ok, result = set_vehicle_day(vehicle_id)

        if ok:
            await update.message.reply_text("☀️ Сохранено: Day.")
            await show_next_vehicle_for_review(update, user_id)
        else:
            await update.message.reply_text(
                f"Ошибка: {result}",
                reply_markup=kb(VEHICLE_ACTION_MENU),
            )
        return

    if text == "🌙 Night":
        ok, result = set_vehicle_night(vehicle_id)

        if ok:
            await update.message.reply_text("🌙 Сохранено: Night.")
            await show_next_vehicle_for_review(update, user_id)
        else:
            await update.message.reply_text(
                f"Ошибка: {result}",
                reply_markup=kb(VEHICLE_ACTION_MENU),
            )
        return

    if text == "🚫 Не паркуется":
        ok, result = set_vehicle_inactive(vehicle_id)

        if ok:
            await update.message.reply_text("🚫 Сохранено: Не паркуется.")
            await show_next_vehicle_for_review(update, user_id)
        else:
            await update.message.reply_text(
                f"Ошибка: {result}",
                reply_markup=kb(VEHICLE_ACTION_MENU),
            )
        return

    await update.message.reply_text(
        "Выберите действие кнопкой.",
        reply_markup=kb(VEHICLE_ACTION_MENU),
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    text = (update.message.text or "").strip()

    lang = user_languages.get(user_id, "ru")

    upsert_resident_account_from_telegram(user, lang)

    # =========================
    # Выбор языка
    # =========================

    if text == "🇷🇺 Русский":
        user_languages[user_id] = "ru"
        lang = "ru"

        if user_id in SUPER_ADMIN_IDS:
            await show_mode_menu(update, lang)
        else:
            user_modes[user_id] = "client"
            await show_client_menu(update, lang)
        return

    if text == "🇺🇦 Українська":
        user_languages[user_id] = "uk"
        lang = "uk"

        if user_id in SUPER_ADMIN_IDS:
            await show_mode_menu(update, lang)
        else:
            user_modes[user_id] = "client"
            await show_client_menu(update, lang)
        return

    if text == "🇬🇧 English":
        user_languages[user_id] = "en"
        lang = "en"

        if user_id in SUPER_ADMIN_IDS:
            await show_mode_menu(update, lang)
        else:
            user_modes[user_id] = "client"
            await show_client_menu(update, lang)
        return

    t = TEXTS[lang]

    # =========================
    # Реестр помещений
    # =========================
    # Вызывается до общего state-router, потому что редактор имеет
    # собственные вложенные шаги и собственную обработку кнопки «Назад».
    if await handle_unit_registry_editor_text(update, user_states, user_id, text):
        return

    # =========================
    # Состояния пользователя
    # =========================

    state = user_states.get(user_id)

    if state == "waiting_apartment":
        if text == "🏠 Главное меню":
            user_states.pop(user_id, None)
            await show_client_menu(update, lang)
            return

        await handle_waiting_apartment(update, user_id, text)
        return

    if isinstance(state, tuple) and state[0] == "confirm_apartment":
        await handle_confirm_apartment(update, user_id, text, lang)
        return

    if state == "admin_waiting_user_id_verify":
        await handle_admin_waiting_user_id(update, user_id, text, "verify")
        return

    if state == "admin_waiting_user_id_unlink":
        await handle_admin_waiting_user_id(update, user_id, text, "unlink")
        return

    if state == "admin_waiting_apartment_lookup":

        if text == "⬅️ Назад":
            user_states.pop(user_id, None)
            await show_admin_menu(update)
            return

        user_states.pop(user_id, None)
        await show_apartment_card(update, user_id, text)
        return

    if isinstance(state, tuple) and state[0] in [
        "admin_confirm_verify_user",
        "admin_confirm_unlink_user",
    ]:
        await handle_admin_confirm_user_action(update, user_id, text)
        return

    if isinstance(state, tuple) and state[0] == "vehicle_select_in_apartment":
        apartment_number = state[1]

        if text == "⬅️ Назад":
            user_states.pop(user_id, None)
            await show_apartment_card(update, user_id, apartment_number)
            return

        vehicles = user_admin_vehicles.get(user_id) or get_apartment_vehicles(apartment_number)

        try:
            selected_index = int(text.strip())
        except ValueError:
            await update.message.reply_text(
                "Нажмите кнопку с номером строки.",
                reply_markup=kb(build_number_keyboard(len(vehicles))),
            )
            return

        if selected_index < 1 or selected_index > len(vehicles):
            await update.message.reply_text(
                "Такой строки нет. Выберите номер из списка.",
                reply_markup=kb(build_number_keyboard(len(vehicles))),
            )
            return

        selected_vehicle = vehicles[selected_index - 1]
        vehicle_id = selected_vehicle[0]

        await show_vehicle_card(update, user_id, vehicle_id)
        return

    if isinstance(state, tuple) and state[0] == "vehicle_card":
        vehicle_id = state[1]

        if text == "⬅️ Назад":
            user_states.pop(user_id, None)
            await show_current_apartment_vehicles(update, user_id)
            return

        if text == "✏️ Статус":
            user_states[user_id] = ("vehicle_edit_status", vehicle_id)
            await update.message.reply_text(
                "Выберите статус:",
                reply_markup=kb(VEHICLE_STATUS_MENU),
            )
            return

        if text == "✏️ Номер":
            user_states[user_id] = ("vehicle_edit_plate", vehicle_id)
            await update.message.reply_text(
                "Введите новый номер автомобиля:",
                reply_markup=kb([["⬅️ Назад"]]),
            )
            return

        if text == "✏️ Марка":
            user_states[user_id] = ("vehicle_edit_model", vehicle_id)
            await update.message.reply_text(
                "Введите новую марку автомобиля:",
                reply_markup=kb([["⬅️ Назад"]]),
            )
            return

        if text == "🏠 Перенести":
            await update.message.reply_text(
                "Перенос в другую квартиру добавим следующим шагом.",
                reply_markup=kb(VEHICLE_EDIT_MENU),
            )
            return

        await update.message.reply_text(
            "Выберите действие кнопкой.",
            reply_markup=kb(VEHICLE_EDIT_MENU),
        )
        return

    if isinstance(state, tuple) and state[0] == "vehicle_edit_status":
        vehicle_id = state[1]

        if text == "⬅️ Назад":
            await show_vehicle_card(update, user_id, vehicle_id)
            return

        mapping = {
            "☀️ Day": "Day",
            "🌙 Night": "Night",
            "🚫 Не паркуется": "Inactive",
            "❓ NULL": "NULL",
        }

        status = mapping.get(text)

        if not status:
            await update.message.reply_text(
                "Выберите статус кнопкой.",
                reply_markup=kb(VEHICLE_STATUS_MENU),
            )
            return

        ok, result = update_vehicle_parking_status(vehicle_id, status)

        if ok:
            await update.message.reply_text("Статус сохранён.")
            await show_vehicle_card(update, user_id, vehicle_id)
        else:
            await update.message.reply_text(
                f"Ошибка: {result}",
                reply_markup=kb(VEHICLE_STATUS_MENU),
            )
        return

    if isinstance(state, tuple) and state[0] == "vehicle_edit_plate":
        vehicle_id = state[1]

        if text == "⬅️ Назад":
            await show_vehicle_card(update, user_id, vehicle_id)
            return

        ok, result = update_vehicle_plate(vehicle_id, text)

        if ok:
            await update.message.reply_text("Номер сохранён.")
            await show_vehicle_card(update, user_id, vehicle_id)
        else:
            await update.message.reply_text(
                f"Ошибка: {result}",
                reply_markup=kb([["⬅️ Назад"]]),
            )
        return

    if isinstance(state, tuple) and state[0] == "vehicle_edit_model":
        vehicle_id = state[1]

        if text == "⬅️ Назад":
            await show_vehicle_card(update, user_id, vehicle_id)
            return

        ok, result = update_vehicle_model(vehicle_id, text)

        if ok:
            await update.message.reply_text("Марка сохранена.")
            await show_vehicle_card(update, user_id, vehicle_id)
        else:
            await update.message.reply_text(
                f"Ошибка: {result}",
                reply_markup=kb([["⬅️ Назад"]]),
            )
        return

    if state == "admin_waiting_agreement_apartment":
        await handle_waiting_agreement_apartment(update, user_states, user_id, text)
        return

    if isinstance(state, tuple) and state[0] == "agreement_card":
        await handle_agreement_card_action(
            update,
            user_states,
            user_id,
            text,
            show_apartment_card,
        )
        return

    if isinstance(state, tuple) and state[0] == "vehicle_review":
        await handle_vehicle_review_action(update, user_id, text)
        return

    # =========================
    # Переключение режимов
    # =========================

    if text in [
        t["client_mode"],
        "👤 Клиентский режим",
        "👤 Режим мешканця",
        "👤 User mode",
    ]:
        user_modes[user_id] = "client"
        await show_client_menu(update, lang)
        return

    if text in [
        t["admin_mode"],
        "🔐 Админ-режим",
        "🔐 Адмін-режим",
        "🔐 Admin mode",
    ]:
        if is_admin_user(user_id):
            user_modes[user_id] = "admin"
            await show_admin_menu(update)
        else:
            await update.message.reply_text("Нет доступа.")
        return

    # =========================
    # Навигация
    # =========================

    if text == "🏠 Главное меню":
        if user_modes.get(user_id) == "admin" and is_admin_user(user_id):
            await show_admin_menu(update)
        else:
            await show_client_menu(update, lang)
        return

    if text == "⬅️ Назад":
        if user_modes.get(user_id) == "admin" and is_admin_user(user_id):
            await show_admin_menu(update)
        else:
            await show_client_menu(update, lang)
        return

    # =========================
    # Клиентский режим
    # =========================

    if text == "🏠 Моя квартира":
        await show_my_apartment(update, user_id)
        return

    if text == "✏️ Изменить квартиру":
        user_states[user_id] = "waiting_apartment"
        await update.message.reply_text("Введите новый номер квартиры:")
        return

    if text == "🚗 Мои автомобили":
        await show_my_vehicles(update, user_id)
        return

    if text in ["🚗 Парковка", "🚗 Parking", "🚗 Паркування"]:
        await update.message.reply_text(
            "🚗 Парковка\n\n"
            "Здесь будут начисления, оплаты и задолженность.",
            reply_markup=kb(CLIENT_MENU_RU),
        )
        return

    if text in ["🔑 Пульты", "🔑 Remotes"]:
        await update.message.reply_text(
            "🔑 Пульты шлагбаума\n\n"
            "Здесь можно будет заказать новый пульт.",
            reply_markup=kb(CLIENT_MENU_RU),
        )
        return

    if text == "📞 Открытие по телефону":
        await update.message.reply_text(
            "📞 Открытие шлагбаума по телефону\n\n"
            "Здесь можно будет зарегистрировать телефон.",
            reply_markup=kb(CLIENT_MENU_RU),
        )
        return

    if text in ["🏗 Благоустройство", "🏗 Благоустрій", "🏗 Improvements"]:
        await update.message.reply_text(
            "🏗 Благоустройство\n\n"
            "Здесь будут сборы и заявки по благоустройству.",
            reply_markup=kb(CLIENT_MENU_RU),
        )
        return

    if text in ["📢 Объявления", "📢 Оголошення", "📢 Announcements"]:
        await update.message.reply_text(
            "📢 Объявления\n\n"
            "Пока объявлений нет.",
            reply_markup=kb(CLIENT_MENU_RU),
        )
        return

    if text in ["📞 Контакты", "📞 Контакти", "📞 Contacts"]:
        await update.message.reply_text(
            "📞 Контакты\n\n"
            "Контакты ОСББ будут добавлены позже.",
            reply_markup=kb(CLIENT_MENU_RU),
        )
        return

    # =========================
    # Админ-режим
    # =========================

    if text == "🏠 Квартиры":
        user_states[user_id] = "admin_waiting_apartment_lookup"

        await update.message.reply_text(
            "Введите номер квартиры:",
            reply_markup=kb([["⬅️ Назад"]]),
        )
        return

    if text == "👥 Жильцы":
        await show_current_apartment_residents(update, user_id)
        return

    if text == "🚗 Авто":
        await show_current_apartment_vehicles(update, user_id)
        return

    if text == "📞 Телефоны":
        apartment_number = user_admin_apartments.get(user_id)
        suffix = f" кв.{apartment_number}" if apartment_number else ""
        await update.message.reply_text(
            f"📞 Телефоны{suffix}\n\n"
            "Раздел будет добавлен позже.",
            reply_markup=kb(APARTMENT_MENU if apartment_number else ADMIN_MENU),
        )
        return

    if text == "🔑 Пульты":
        apartment_number = user_admin_apartments.get(user_id)
        suffix = f" кв.{apartment_number}" if apartment_number else ""
        await update.message.reply_text(
            f"🔑 Пульты{suffix}\n\n"
            "Раздел будет добавлен позже.",
            reply_markup=kb(APARTMENT_MENU if apartment_number else ADMIN_MENU),
        )
        return

    if text == "👥 Пользователи":
        await show_users_menu(update)
        return

    if text == "📋 Все пользователи":
        await show_resident_list(update, "Все пользователи", "all")
        return

    if text == "🏠 Без квартиры":
        await show_resident_list(update, "Без квартиры", "without_apartment")
        return

    if text == "⏳ Самоподтверждённые":
        await show_resident_list(update, "Самоподтверждённые", "self_confirmed")
        return

    if text == "✅ Проверенные оператором":
        await show_resident_list(update, "Проверенные оператором", "operator_verified")
        return

    if text == "🔎 Проверить пользователя":
        await ask_user_to_verify(update)
        return

    if text == "❌ Отвязать квартиру":
        await ask_user_to_unlink(update)
        return

    if text == "🚗 Автомобили":
        await show_vehicle_menu(update)
        return
    if await handle_vehicle_full_list_text(update, user_states, user_id, text):
        return
    if text == "📋 Все автомобили":
        rows = get_vehicles_by_status("all", limit=50)
        await update.message.reply_text(
            format_vehicles_admin_list("Все автомобили", rows),
            reply_markup=kb(VEHICLE_REVIEW_MENU),
        )
        return

    if text == "❓ Без статуса":
        rows = get_vehicles_by_status("missing", limit=50)
        await update.message.reply_text(
            format_vehicles_admin_list("Автомобили без статуса", rows),
            reply_markup=kb(VEHICLE_REVIEW_MENU),
        )
        return

    if text == "☀️ Day":
        rows = get_vehicles_by_status("Day", limit=50)
        await update.message.reply_text(
            format_vehicles_admin_list("Автомобили Day", rows),
            reply_markup=kb(VEHICLE_REVIEW_MENU),
        )
        return

    if text == "🌙 Night":
        rows = get_vehicles_by_status("Night", limit=50)
        await update.message.reply_text(
            format_vehicles_admin_list("Автомобили Night", rows),
            reply_markup=kb(VEHICLE_REVIEW_MENU),
        )
        return

    if text == "🚫 Не паркуется":
        rows = get_vehicles_by_status("Inactive", limit=50)
        await update.message.reply_text(
            format_vehicles_admin_list("Не паркуется", rows),
            reply_markup=kb(VEHICLE_REVIEW_MENU),
        )
        return

    if text == "📊 Статистика авто":
        await show_vehicle_stats(update)
        return

    if await handle_agreement_menu_text(update, user_states, user_id, text):
        return

    if text == "🔑 Заявки на пульты":
        await update.message.reply_text(
            "🔑 Заявки на пульты\n\n"
            "Здесь будет обработка заказов пультов.",
            reply_markup=kb(ADMIN_MENU),
        )
        return

    if text == "📞 Телефонный доступ":
        await update.message.reply_text(
            "📞 Телефонный доступ\n\n"
            "Здесь будут заявки на открытие шлагбаума звонком.",
            reply_markup=kb(ADMIN_MENU),
        )
        return

    if text == "💳 Платежи":
        await update.message.reply_text(
            "💳 Платежи\n\n"
            "Здесь будет учёт оплат.",
            reply_markup=kb(ADMIN_MENU),
        )
        return

    if text == "📊 Отчёты":
        await update.message.reply_text(
            "📊 Отчёты\n\n"
            "Здесь будут отчёты по ОСББ.",
            reply_markup=kb(ADMIN_MENU),
        )
        return

    if text == "⚙️ Настройки":
        await update.message.reply_text(
            "⚙️ Настройки\n\n"
            "Здесь будут настройки бота и администраторов.",
            reply_markup=kb(ADMIN_MENU),
        )
        return
    # =========================
    # SPECIAL MODES
    # =========================

    if await handle_vehicle_verification_text(
        update,
        user_states,
        user_id,
        text,
    ):
        return
    
    if await handle_vehicle_card_editor_text(update, user_states, user_id, text):
        return
    if await handle_audit_viewer_text(update, user_states, user_id, text):
        return
    # =========================
    # fallback
    # =========================

    await update.message.reply_text(
        f"Вы нажали: {text}",
        reply_markup=kb(CLIENT_MENU_RU),
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    )

    print("OSBB bot started.")
    app.run_polling()


if __name__ == "__main__":
    main()
