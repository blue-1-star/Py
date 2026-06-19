from telegram import Update, ReplyKeyboardMarkup

from Bots.db_access import (
    get_verification_stats,
    format_verification_stats,
    get_next_apartment_for_verification,
    get_apartments_by_verification_status,
    set_apartment_verification_status,
    format_verification_apartment_list,
    format_apartment_agreement_card,
    get_agreement_dashboard,
    format_agreement_dashboard,
    apply_agreement_suggestion,
)


AGREEMENT_MENU = [
    ["▶️ Продолжить"],
    ["🏠 Найти квартиру"],
    ["📌 Сводка"],
    ["⚠️ Конфликты", "⏳ Отложенные"],
    ["📊 Статистика"],
    ["⬅️ Назад"],
]

AGREEMENT_ACTION_MENU = [
    ["✅ Согласовать"],
    ["⏳ Отложить", "⚠️ Конфликт"],
    ["✏️ Исправить"],
    ["⏭ Пропустить"],
    ["⬅️ Назад"],
]

user_agreement_skips = {}


def kb(buttons):
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_skipped_apartments(user_id: int):
    return user_agreement_skips.setdefault(user_id, set())


async def show_agreement_menu(update: Update):
    stats = get_verification_stats()

    await update.message.reply_text(
        format_verification_stats(stats) + "\n\nВыберите действие:",
        reply_markup=kb(AGREEMENT_MENU),
    )


async def show_agreement_stats(update: Update):
    stats = get_verification_stats()

    await update.message.reply_text(
        format_verification_stats(stats),
        reply_markup=kb(AGREEMENT_MENU),
    )


async def show_agreement_dashboard(update: Update):
    dashboard = get_agreement_dashboard()

    await update.message.reply_text(
        format_agreement_dashboard(dashboard),
        reply_markup=kb(AGREEMENT_MENU),
    )


async def show_agreement_card(update: Update, user_states: dict, user_id: int, apartment_number: str):
    user_states[user_id] = ("agreement_card", str(apartment_number))

    await update.message.reply_text(
        format_apartment_agreement_card(apartment_number),
        reply_markup=kb(AGREEMENT_ACTION_MENU),
    )


async def show_next_agreement_apartment(update: Update, user_states: dict, user_id: int):
    skipped = get_skipped_apartments(user_id)
    row = get_next_apartment_for_verification(skipped)

    if not row:
        user_states.pop(user_id, None)

        await update.message.reply_text(
            "Новых квартир в текущей сессии больше нет.\n\n"
            "Если нужно начать просмотр заново, нажмите 🤝 Согласование.",
            reply_markup=kb(AGREEMENT_MENU),
        )
        return

    apartment_number = row[2]
    await show_agreement_card(update, user_states, user_id, apartment_number)


async def show_agreement_list(update: Update, title: str, status: str):
    rows = get_apartments_by_verification_status(status, limit=50)

    await update.message.reply_text(
        format_verification_apartment_list(title, rows),
        reply_markup=kb(AGREEMENT_MENU),
    )


async def handle_waiting_agreement_apartment(update: Update, user_states: dict, user_id: int, text: str):
    if text == "⬅️ Назад":
        user_states.pop(user_id, None)
        await show_agreement_menu(update)
        return

    user_states.pop(user_id, None)
    await show_agreement_card(update, user_states, user_id, text)


async def handle_agreement_card_action(
    update: Update,
    user_states: dict,
    user_id: int,
    text: str,
    show_apartment_card_callback,
):
    state = user_states.get(user_id)

    if not (isinstance(state, tuple) and state[0] == "agreement_card"):
        user_states.pop(user_id, None)
        await show_agreement_menu(update)
        return

    apartment_number = state[1]

    if text == "⬅️ Назад":
        user_states.pop(user_id, None)
        await show_agreement_menu(update)
        return

    if text == "⏭ Пропустить":
        get_skipped_apartments(user_id).add(str(apartment_number))
        await show_next_agreement_apartment(update, user_states, user_id)
        return

    if text == "✏️ Исправить":
        user_states.pop(user_id, None)
        await show_apartment_card_callback(update, user_id, apartment_number)
        return

    if text == "✅ Согласовать":
        ok, result = apply_agreement_suggestion(
            apartment_number,
            verified_by=user_id,
        )

        if ok:
            applied = result.get("applied") if isinstance(result, dict) else None

            if applied and applied.get("action") == "created":
                await update.message.reply_text(
                    f"✅ Квартира {apartment_number} согласована.\n"
                    f"Создано авто: {applied.get('plate')} | "
                    f"{applied.get('model') or '-'} | "
                    f"{applied.get('parking_time') or 'NULL'}"
                )
            elif applied and applied.get("action") == "updated":
                await update.message.reply_text(
                    f"✅ Квартира {apartment_number} согласована.\n"
                    "Данные авто обновлены."
                )
            else:
                await update.message.reply_text(
                    f"✅ Квартира {apartment_number} согласована."
                )

            await show_next_agreement_apartment(update, user_states, user_id)
        else:
            await update.message.reply_text(
                f"Ошибка: {result}",
                reply_markup=kb(AGREEMENT_ACTION_MENU),
            )
        return

    if text == "⏳ Отложить":
        ok, result = set_apartment_verification_status(
            apartment_number,
            "deferred",
            verified_by=user_id,
        )

        if ok:
            await update.message.reply_text(f"⏳ Квартира {apartment_number} отложена.")
            await show_next_agreement_apartment(update, user_states, user_id)
        else:
            await update.message.reply_text(
                f"Ошибка: {result}",
                reply_markup=kb(AGREEMENT_ACTION_MENU),
            )
        return

    if text == "⚠️ Конфликт":
        ok, result = set_apartment_verification_status(
            apartment_number,
            "conflict",
            verified_by=user_id,
        )

        if ok:
            await update.message.reply_text(f"⚠️ Квартира {apartment_number}: конфликт.")
            await show_next_agreement_apartment(update, user_states, user_id)
        else:
            await update.message.reply_text(
                f"Ошибка: {result}",
                reply_markup=kb(AGREEMENT_ACTION_MENU),
            )
        return

    await update.message.reply_text(
        "Выберите действие кнопкой.",
        reply_markup=kb(AGREEMENT_ACTION_MENU),
    )


async def handle_agreement_menu_text(update: Update, user_states: dict, user_id: int, text: str):
    if text == "🤝 Согласование":
        user_agreement_skips.pop(user_id, None)
        await show_agreement_menu(update)
        return True

    if text == "▶️ Продолжить":
        await show_next_agreement_apartment(update, user_states, user_id)
        return True

    if text == "🏠 Найти квартиру":
        user_states[user_id] = "admin_waiting_agreement_apartment"

        await update.message.reply_text(
            "Введите номер квартиры:",
            reply_markup=kb([["⬅️ Назад"]]),
        )
        return True

    if text == "📌 Сводка":
        await show_agreement_dashboard(update)
        return True

    if text == "⚠️ Конфликты":
        await show_agreement_list(update, "Конфликты", "conflict")
        return True

    if text == "⏳ Отложенные":
        await show_agreement_list(update, "Отложенные", "deferred")
        return True

    if text == "📊 Статистика":
        await show_agreement_stats(update)
        return True

    return False
