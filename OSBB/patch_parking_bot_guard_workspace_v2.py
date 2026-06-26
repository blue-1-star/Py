"""
Подключение отдельного кабинета охраны к Bots/parking_bot.py.

Изменяет только код бота при --apply:
- добавляет импорт guard_workspace;
- показывает «🛡 Пост охраны O» только пользователю с правом GUARD_O;
- обычный охранник после выбора языка получает выбор рабочего кабинета,
  а не общий админ-раздел;
- маршрутизирует guard state machine раньше старых клиентских/админских веток;
- оставляет админ-режим прежним для ADMIN_IDS / SUPER_ADMIN_IDS.

По умолчанию dry-run и исходный bot не меняется.
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
    if (
        user_modes.get(user_id) == "guard"
        or (
            isinstance(guard_state, dict)
            and guard_state.get("_module") == "guard_workspace_o"
        )
    ):
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

HOME_GUARD = """
    if text == "🏠 Главное меню":
        if user_modes.get(user_id) == "guard":
            await show_guard_workspace(update, user_states, user_id)
            return
"""

BACK_GUARD = """
    if text == "⬅️ Назад":
        if user_modes.get(user_id) == "guard":
            await show_guard_workspace(update, user_states, user_id)
            return
"""


def replace_between(source: str, start: str, end: str, replacement: str) -> str:
    pos_start = source.find(start)
    if pos_start < 0:
        raise RuntimeError(f"Не найден блок: {start}")
    pos_end = source.find(end, pos_start)
    if pos_end < 0:
        raise RuntimeError(f"Не найден конец блока: {end}")
    return source[:pos_start] + replacement.rstrip() + "\n\n" + source[pos_end:]


def add_import(source: str) -> tuple[str, bool]:
    if "from handlers.guard_workspace import (" in source:
        return source, False

    anchor = "from handlers.audit_viewer import handle_audit_viewer_text\n"
    if anchor not in source:
        raise RuntimeError("Не найден импортный якорь handlers.audit_viewer.")
    return source.replace(anchor, anchor + GUARD_IMPORT, 1), True


def patch(source: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    source, added_import = add_import(source)
    if added_import:
        changes.append("guard_workspace import")

    if "async def show_mode_menu(update: Update, lang: str):" not in source:
        raise RuntimeError("Не найдена функция show_mode_menu().")
    mode_block = source[
        source.find("async def show_mode_menu(update: Update, lang: str):"):
        source.find("async def show_client_menu(")
    ]
    if "🛡 Пост охраны O" not in mode_block:
        source = replace_between(
            source,
            "async def show_mode_menu(update: Update, lang: str):",
            "async def show_client_menu(",
            SHOW_MODE,
        )
        changes.append("mode menu with guard workspace")

    old_language_gate = "if user_id in SUPER_ADMIN_IDS:"
    new_language_gate = (
        "if is_admin_user(user_id) or "
        "has_guard_workspace_access(user_id, cashbox_code=\"O\"):"
    )
    if old_language_gate in source:
        count = source.count(old_language_gate)
        if count != 3:
            raise RuntimeError(
                f"Ожидалось 3 language gates, найдено {count}. Исходник не изменён."
            )
        source = source.replace(old_language_gate, new_language_gate)
        changes.append("language gate for guard users")

    route_anchor = (
        "    t = TEXTS[lang]\n\n"
        "    # =========================\n"
        "    # Состояния пользователя\n"
    )
    if route_anchor in source and "Отдельный рабочий кабинет охраны" not in source:
        source = source.replace(
            route_anchor,
            "    t = TEXTS[lang]\n\n" + GUARD_ROUTE
            + "    # =========================\n"
              "    # Состояния пользователя\n",
            1,
        )
        changes.append("guard state router")

    admin_switch_anchor = (
        "    if text in [\n"
        "        t[\"admin_mode\"],\n"
    )
    if admin_switch_anchor in source and 'if text == "🛡 Пост охраны O":' not in source:
        source = source.replace(
            admin_switch_anchor,
            GUARD_MODE_SWITCH + admin_switch_anchor,
            1,
        )
        changes.append("guard mode switch")

    navigation_start = source.find(
        "# =========================\n"
        "    # Навигация\n"
    )
    if navigation_start < 0:
        raise RuntimeError("Не найден раздел навигации в message_handler().")

    global_home = source.find('    if text == "🏠 Главное меню":', navigation_start)
    global_back = source.find('    if text == "⬅️ Назад":', navigation_start)
    if global_home < 0 or global_back < 0:
        raise RuntimeError("Не найдены глобальные кнопки Главное меню / Назад.")

    home_end = source.find('    if text == "⬅️ Назад":', global_home)
    home_block = source[global_home:home_end]
    if 'user_modes.get(user_id) == "guard"' not in home_block:
        source = source[:global_home] + HOME_GUARD + source[global_home:]
        changes.append("guard home navigation")

        # Source offset moved after insertion.
        global_back = source.find('    if text == "⬅️ Назад":', global_home)

    back_end = source.find(
        "# =========================\n"
        "    # Клиентский режим",
        global_back,
    )
    back_block = source[global_back:back_end]
    if 'user_modes.get(user_id) == "guard"' not in back_block:
        source = source[:global_back] + BACK_GUARD + source[global_back:]
        changes.append("guard back navigation")

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
    print("PATCH PARKING BOT: GUARD WORKSPACE")
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
