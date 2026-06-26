"""
Подключение отдельного кабинета охраны к Bots/parking_bot.py — версия с выходом из кабинета.

Использует максимально устойчивые точки вставки:
- импорт после audit_viewer;
- show_mode_menu;
- три language gate;
- перед строкой state = user_states.get(user_id) в message_handler;
- перед веткой выбора админ-режима.

Не меняет исходный parking_bot.py без --apply.
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BOT_FILE = ROOT / "Bots" / "parking_bot.py"
GUARD_FILE = ROOT / "Bots" / "handlers" / "guard_workspace.py"

GUARD_IMPORT = (
    "from handlers.guard_workspace import (\n"
    "    handle_guard_workspace_text,\n"
    "    has_guard_workspace_access,\n"
    "    show_guard_workspace,\n"
    ")\n"
)

SHOW_MODE = """
async def show_mode_menu(update: Update, lang: str):
    t = TEXTS[lang]
    user_id = update.effective_user.id

    buttons = [[t["client_mode"]]]
    if has_guard_workspace_access(user_id, cashbox_code="O"):
        buttons.append(["🛡 Пост охраны O"])
    if is_admin_user(user_id):
        buttons.append([t["admin_mode"]])

    await update.message.reply_text(
        t["mode"],
        reply_markup=kb(buttons),
    )
"""

GUARD_ROUTE = """
    # =========================
    # Отдельный рабочий кабинет охраны
    # =========================
    guard_state = user_states.get(user_id)
    guard_active = (
        user_modes.get(user_id) == "guard"
        or (
            isinstance(guard_state, dict)
            and guard_state.get("_module") == "guard_workspace_o"
        )
    )

    # «Главное меню» должно выйти из рабочего кабинета, а не открыть
    # его повторно. Это возвращает пользователя к выбору доступных режимов.
    if guard_active and text in {"🏠 Главное меню", "⬅️ Назад"}:
        user_states.pop(user_id, None)
        user_modes.pop(user_id, None)
        await show_mode_menu(update, lang)
        return

    if guard_active:
        handled = await handle_guard_workspace_text(
            update, user_states, user_id, text, lang=lang
        )
        if handled:
            return

"""

GUARD_MODE_SWITCH = """
    if text == "🛡 Пост охраны O":
        if has_guard_workspace_access(user_id, cashbox_code="O"):
            user_modes[user_id] = "guard"
            user_states.pop(user_id, None)
            await show_guard_workspace(update, user_states, user_id)
        else:
            await update.message.reply_text("Нет доступа к посту охраны O.")
        return

"""


def replace_between(source: str, start: str, end: str, replacement: str) -> str:
    left = source.find(start)
    if left < 0:
        raise RuntimeError(f"Не найден блок начала: {start}")
    right = source.find(end, left)
    if right < 0:
        raise RuntimeError(f"Не найден блок конца: {end}")
    return source[:left] + replacement.rstrip() + "\n\n" + source[right:]


def add_import(source: str) -> tuple[str, bool]:
    if "from handlers.guard_workspace import (" in source:
        return source, False
    anchor = "from handlers.audit_viewer import handle_audit_viewer_text\n"
    if anchor not in source:
        raise RuntimeError("Не найден импортный якорь handlers.audit_viewer.")
    return source.replace(anchor, anchor + GUARD_IMPORT, 1), True


def insert_guard_router(source: str) -> tuple[str, bool]:
    if "handle_guard_workspace_text(" in source:
        return source, False

    handler_start = source.find("async def message_handler(")
    if handler_start < 0:
        raise RuntimeError("Не найдена функция message_handler().")

    state_line = "    state = user_states.get(user_id)"
    state_pos = source.find(state_line, handler_start)
    if state_pos < 0:
        raise RuntimeError(
            "Не найдена строка state = user_states.get(user_id) "
            "внутри message_handler()."
        )

    # The guard route is inserted immediately before normal state processing.
    # At this point lang and text are already resolved.
    return source[:state_pos] + GUARD_ROUTE + source[state_pos:], True


def insert_guard_mode_switch(source: str) -> tuple[str, bool]:
    if 'if text == "🛡 Пост охраны O":' in source:
        return source, False

    handler_start = source.find("async def message_handler(")
    if handler_start < 0:
        raise RuntimeError("Не найдена функция message_handler().")

    admin_label_pos = source.find('t["admin_mode"]', handler_start)
    if admin_label_pos < 0:
        raise RuntimeError(
            'Не найдена ветка t["admin_mode"] в message_handler().'
        )

    branch_start = source.rfind("    if text", handler_start, admin_label_pos)
    if branch_start < 0:
        raise RuntimeError(
            "Не найдена строка начала ветки выбора админ-режима."
        )

    return source[:branch_start] + GUARD_MODE_SWITCH + source[branch_start:], True


def patch(source: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    source, changed = add_import(source)
    if changed:
        changes.append("guard_workspace import")

    mode_start = source.find("async def show_mode_menu(update: Update, lang: str):")
    mode_end = source.find("async def show_client_menu(", mode_start)
    if mode_start < 0 or mode_end < 0:
        raise RuntimeError("Не найдена функция show_mode_menu().")
    if "🛡 Пост охраны O" not in source[mode_start:mode_end]:
        source = replace_between(
            source,
            "async def show_mode_menu(update: Update, lang: str):",
            "async def show_client_menu(",
            SHOW_MODE,
        )
        changes.append("mode menu with guard workspace")

    old_gate = "if user_id in SUPER_ADMIN_IDS:"
    new_gate = (
        "if is_admin_user(user_id) or "
        "has_guard_workspace_access(user_id, cashbox_code=\"O\"):"
    )
    if old_gate in source:
        count = source.count(old_gate)
        if count != 3:
            raise RuntimeError(
                f"Ожидалось 3 language gates, найдено {count}. "
                "Исходник не изменён."
            )
        source = source.replace(old_gate, new_gate)
        changes.append("language gate for guard users")

    source, changed = insert_guard_router(source)
    if changed:
        changes.append("guard state router")

    source, changed = insert_guard_mode_switch(source)
    if changed:
        changes.append("guard mode switch")

    required = [
        "from handlers.guard_workspace import (",
        "has_guard_workspace_access(user_id, cashbox_code=\"O\")",
        "handle_guard_workspace_text(",
        'if text == "🛡 Пост охраны O":',
    ]
    missing = [marker for marker in required if marker not in source]
    if missing:
        raise RuntimeError(
            "Патч не собран полностью. Нет маркеров: " + ", ".join(missing)
        )

    return source, changes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    print("=" * 100)
    print("PATCH PARKING BOT: GUARD WORKSPACE V4")
    print("=" * 100)
    print("Bot:", BOT_FILE)
    print("Apply:", args.apply)

    if not GUARD_FILE.exists():
        raise SystemExit(f"Сначала разместите guard_workspace.py: {GUARD_FILE}")
    if not BOT_FILE.exists():
        raise SystemExit(f"Не найден parking_bot.py: {BOT_FILE}")

    original = BOT_FILE.read_text(encoding="utf-8")
    try:
        patched, changes = patch(original)
        compile(patched, str(BOT_FILE), "exec")
    except Exception as exc:
        raise SystemExit(
            f"Проверка патча не пройдена: {exc}\n"
            "Исходный parking_bot.py не изменён."
        )

    print("Changes:")
    for item in changes or ["already patched"]:
        print(" -", item)
    print("Changes needed:", patched != original)

    if not args.apply:
        print("DRY RUN COMPLETED - NO CHANGES SAVED")
        return

    if patched == original:
        print("ALREADY PATCHED - NO FILE CHANGE")
        return

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = BOT_FILE.with_name(
        f"{BOT_FILE.stem}_before_guard_workspace_{stamp}{BOT_FILE.suffix}"
    )
    shutil.copy2(BOT_FILE, backup)
    BOT_FILE.write_text(patched, encoding="utf-8")
    print("APPLIED")
    print("Backup:", backup)
    print("Updated:", BOT_FILE)


if __name__ == "__main__":
    main()
