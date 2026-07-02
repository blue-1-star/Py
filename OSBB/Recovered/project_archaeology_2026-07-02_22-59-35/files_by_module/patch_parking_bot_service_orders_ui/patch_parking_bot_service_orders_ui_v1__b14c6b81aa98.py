"""
Runtime patch for the isolated live service sandbox.

The patch is applied to Bots/parking_bot.py in memory only:
- client_portal_v2 -> client_portal_v3 (combined resident button);
- adds a permission-based service-operator mode;
- routes resident and operator service dialogs before legacy handlers;
- leaves source parking_bot.py unchanged.
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BOT_FILE = ROOT / "Bots" / "parking_bot.py"
WORKSPACE_FILE = ROOT / "Bots" / "handlers" / "service_orders_workspace.py"
PORTAL_FILE = ROOT / "Bots" / "handlers" / "client_portal_v3.py"

SERVICE_IMPORT = (
    "from handlers.service_orders_workspace import (\n"
    "    handle_service_orders_text,\n"
    "    has_service_workspace_access,\n"
    "    show_service_operator_workspace,\n"
    ")\n"
)

SHOW_MODE = """
async def show_mode_menu(update: Update, lang: str):
    t = TEXTS[lang]
    user_id = update.effective_user.id

    buttons = [[t["client_mode"]]]
    if has_guard_workspace_access(user_id, cashbox_code="O"):
        buttons.append(["🛡 Пост охраны O"])
    if has_service_workspace_access(user_id):
        buttons.append(["🔑 Оператор услуг"])
    if is_admin_user(user_id):
        buttons.append([t["admin_mode"]])

    await update.message.reply_text(
        t["mode"],
        reply_markup=kb(buttons),
    )
"""

SERVICE_ACTIVE_ROUTE = """
    # =========================
    # Операторский кабинет услуг
    # =========================
    service_state = user_states.get(user_id)
    service_active = (
        user_modes.get(user_id) == "service_operator"
        or (
            isinstance(service_state, dict)
            and service_state.get("_module") == "service_orders_ui"
            and service_state.get("area") == "operator"
        )
    )

    if service_active and text in {"🏠 Главное меню", "🏠 Головне меню", "🏠 Main menu", "⬅️ Назад"}:
        user_states.pop(user_id, None)
        user_modes.pop(user_id, None)
        await show_mode_menu(update, lang)
        return

    service_global_switch = {
        t["client_mode"],
        t["admin_mode"],
        "👤 Клиентский режим", "👤 Режим мешканця", "👤 User mode",
        "🔐 Админ-режим", "🔐 Адмін-режим", "🔐 Admin mode",
        "🛡 Пост охраны O",
        "🔑 Оператор услуг", "🔑 Оператор послуг", "🔑 Service operator",
        "🔄 Сменить режим", "🔄 Змінити режим", "🔄 Switch mode",
    }
    if service_active and text not in service_global_switch:
        handled = await handle_service_orders_text(
            update,
            user_states,
            user_id,
            text,
            lang=lang,
            user_mode=user_modes.get(user_id),
        )
        if handled:
            return

"""

SERVICE_GENERAL_ROUTE = """
    # =========================
    # Явная смена рабочего режима
    # =========================
    if text in {"🔄 Сменить режим", "🔄 Змінити режим", "🔄 Switch mode"}:
        user_states.pop(user_id, None)
        user_modes.pop(user_id, None)
        await show_mode_menu(update, lang)
        return

    # =========================
    # Заказы услуг: житель и оператор
    # =========================
    if await handle_service_orders_text(
        update,
        user_states,
        user_id,
        text,
        lang=lang,
        user_mode=user_modes.get(user_id),
    ):
        return

"""

SERVICE_MODE_SWITCH = """
    if text == "🔑 Оператор услуг":
        if has_service_workspace_access(user_id):
            user_modes[user_id] = "service_operator"
            user_states.pop(user_id, None)
            await show_service_operator_workspace(
                update, user_states, user_id, lang=lang
            )
        else:
            await update.message.reply_text("Нет доступа к операторскому кабинету услуг.")
        return

"""


def replace_between(source: str, start: str, end: str, replacement: str) -> str:
    left = source.find(start)
    if left < 0:
        raise RuntimeError(f"Не найдено начало блока: {start}")
    right = source.find(end, left)
    if right < 0:
        raise RuntimeError(f"Не найден конец блока: {end}")
    return source[:left] + replacement.rstrip() + "\n\n" + source[right:]


def add_import(source: str) -> tuple[str, bool]:
    if "from handlers.service_orders_workspace import (" in source:
        return source, False
    anchor = "from handlers.guard_workspace import (\n"
    pos = source.find(anchor)
    if pos >= 0:
        close = source.find(")\n", pos)
        if close >= 0:
            close += 2
            return source[:close] + SERVICE_IMPORT + source[close:], True

    anchor = "from handlers.audit_viewer import handle_audit_viewer_text\n"
    if anchor not in source:
        raise RuntimeError("Не найден импортный якорь для service_orders_workspace.")
    return source.replace(anchor, anchor + SERVICE_IMPORT, 1), True


def swap_client_portal(source: str) -> tuple[str, bool]:
    old = "from handlers.client_portal_v2 import ("
    new = "from handlers.client_portal_v3 import ("
    if new in source:
        return source, False
    if old not in source:
        raise RuntimeError(
            "Ожидался импорт client_portal_v2 после v2-switcher. "
            "Исходник не изменён."
        )
    return source.replace(old, new, 1), True


def patch_show_mode(source: str) -> tuple[str, bool]:
    start = source.find("async def show_mode_menu(update: Update, lang: str):")
    end = source.find("async def show_client_menu(", start)
    if start < 0 or end < 0:
        raise RuntimeError("Не найдена show_mode_menu().")
    old = source[start:end]
    if "has_service_workspace_access(user_id)" in old:
        return source, False
    return replace_between(
        source,
        "async def show_mode_menu(update: Update, lang: str):",
        "async def show_client_menu(",
        SHOW_MODE,
    ), True


def patch_language_gates(source: str) -> tuple[str, bool]:
    new_gate = (
        "if is_admin_user(user_id) or "
        "has_guard_workspace_access(user_id, cashbox_code=\"O\") or "
        "has_service_workspace_access(user_id):"
    )
    if new_gate in source:
        return source, False

    old_gate = (
        "if is_admin_user(user_id) or "
        "has_guard_workspace_access(user_id, cashbox_code=\"O\"):"
    )
    count = source.count(old_gate)
    if count != 3:
        raise RuntimeError(
            "Ожидалось 3 language-gate после guard patch, найдено "
            f"{count}."
        )
    return source.replace(old_gate, new_gate), True


def insert_active_router(source: str) -> tuple[str, bool]:
    if "# Операторский кабинет услуг" in source:
        return source, False
    handler_start = source.find("async def message_handler(")
    if handler_start < 0:
        raise RuntimeError("Не найдена message_handler().")
    marker = "    state = user_states.get(user_id)"
    pos = source.find(marker, handler_start)
    if pos < 0:
        raise RuntimeError("Не найдена точка вставки state = user_states.get(user_id).")
    return source[:pos] + SERVICE_ACTIVE_ROUTE + source[pos:], True


def insert_general_router(source: str) -> tuple[str, bool]:
    if "# Заказы услуг: житель и оператор" in source:
        return source, False
    marker = (
        "    # =========================\n"
        "    # Клиентский кабинет / заявки на пульты\n"
        "    # =========================\n"
    )
    if marker not in source:
        raise RuntimeError(
            "Не найден клиентский router. Нужен существующий client portal patch."
        )
    return source.replace(marker, SERVICE_GENERAL_ROUTE + marker, 1), True


def insert_mode_switch(source: str) -> tuple[str, bool]:
    if 'if text == "🔑 Оператор услуг":' in source:
        return source, False
    marker = '    if text == "🛡 Пост охраны O":\n'
    if marker not in source:
        raise RuntimeError("Не найдена ветка выбора поста охраны O.")
    return source.replace(marker, SERVICE_MODE_SWITCH + marker, 1), True


def patch(source: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    for operation, label in (
        (add_import, "service workspace import"),
        (swap_client_portal, "client portal v3"),
        (patch_show_mode, "mode menu with service operator"),
        (patch_language_gates, "language gate for service operators"),
        (insert_active_router, "service operator state router"),
        (insert_general_router, "resident/service general router"),
        (insert_mode_switch, "service operator mode switch"),
    ):
        source, changed = operation(source)
        if changed:
            changes.append(label)

    required = [
        "from handlers.service_orders_workspace import (",
        "from handlers.client_portal_v3 import (",
        "has_service_workspace_access(user_id)",
        "show_service_operator_workspace(",
        "handle_service_orders_text(",
        'if text == "🔑 Оператор услуг":',
        'if text in {"🔄 Сменить режим", "🔄 Змінити режим", "🔄 Switch mode"}:',
    ]
    missing = [item for item in required if item not in source]
    if missing:
        raise RuntimeError("Патч собран не полностью: " + ", ".join(missing))

    return source, changes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    print("=" * 100)
    print("PATCH PARKING BOT: SERVICE ORDERS UI V1")
    print("=" * 100)
    print("Apply:", args.apply)

    for path in (BOT_FILE, WORKSPACE_FILE, PORTAL_FILE):
        if not path.exists():
            print("Не найден:", path)
            return 1

    original = BOT_FILE.read_text(encoding="utf-8")
    try:
        patched, changes = patch(original)
        compile(patched, str(BOT_FILE), "exec")
    except Exception as exc:
        print("Patch check FAILED:", exc)
        return 1

    print("Changes:", "; ".join(changes or ["already patched"]))
    print("Changes needed:", patched != original)
    if not args.apply:
        print("DRY RUN COMPLETED - NO FILES CHANGED")
        return 0
    if patched == original:
        print("ALREADY PATCHED - NO FILE CHANGE")
        return 0

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = BOT_FILE.with_name(f"{BOT_FILE.stem}_before_service_orders_ui_{stamp}{BOT_FILE.suffix}")
    shutil.copy2(BOT_FILE, backup)
    BOT_FILE.write_text(patched, encoding="utf-8")
    print("APPLIED")
    print("Backup:", backup)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
