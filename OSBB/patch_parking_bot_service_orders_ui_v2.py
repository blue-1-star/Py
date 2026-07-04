#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
patch_parking_bot_service_orders_ui_v2.py

Permanent promotion of the old live-services Runner wiring into Bots/parking_bot.py.

Fixed v2:
- inserts service-active route only AFTER `lang = ...` and `t = TEXTS[lang]`,
  so `t["client_mode"]` is always defined;
- keeps dry-run by default;
- creates preview/diff/report in OSBB/Recovered;
- backs up parking_bot.py before --apply;
- does not touch DB and does not launch bot.
"""

from __future__ import annotations

import argparse
import difflib
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BOT_FILE = ROOT / "Bots" / "parking_bot.py"
WORKSPACE_FILE = ROOT / "Bots" / "handlers" / "service_orders_workspace.py"
PORTAL_FILE = ROOT / "Bots" / "handlers" / "client_portal_v3.py"
RECOVERED_DIR = ROOT / "Recovered"

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
    if text in {"🔑 Оператор услуг", "🔑 Оператор послуг", "🔑 Service operator"}:
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


def stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def find_function_block(source: str, signature: str, next_signature: str | None = None) -> tuple[int, int]:
    start = source.find(signature)
    if start < 0:
        raise RuntimeError(f"Не найдена функция: {signature}")

    if next_signature:
        end = source.find(next_signature, start + len(signature))
        if end >= 0:
            return start, end

    search_from = start + len(signature)
    candidates = []
    for marker in ("\nasync def ", "\ndef "):
        pos = source.find(marker, search_from)
        if pos >= 0:
            candidates.append(pos + 1)
    if not candidates:
        return start, len(source)
    return start, min(candidates)


def add_service_import(source: str) -> tuple[str, bool]:
    if "from handlers.service_orders_workspace import (" in source:
        return source, False

    guard_anchor = "from handlers.guard_workspace import (\n"
    pos = source.find(guard_anchor)
    if pos >= 0:
        close = source.find(")\n", pos)
        if close >= 0:
            close += 2
            return source[:close] + SERVICE_IMPORT + source[close:], True

    audit_anchor = "from handlers.audit_viewer import handle_audit_viewer_text\n"
    if audit_anchor in source:
        return source.replace(audit_anchor, audit_anchor + SERVICE_IMPORT, 1), True

    raise RuntimeError("Не найден безопасный импортный якорь для service_orders_workspace.")


def swap_client_portal_to_v3(source: str) -> tuple[str, bool]:
    if "from handlers.client_portal_v3 import (" in source:
        return source, False

    for old in (
        "from handlers.client_portal_v2 import (",
        "from handlers.client_portal import (",
    ):
        if old in source:
            return source.replace(old, "from handlers.client_portal_v3 import (", 1), True

    raise RuntimeError("Не найден импорт client_portal/client_portal_v2 для замены на client_portal_v3.")


def patch_show_mode_menu(source: str) -> tuple[str, bool]:
    start, end = find_function_block(
        source,
        "async def show_mode_menu(update: Update, lang: str):",
        "async def show_client_menu(",
    )
    current = source[start:end]
    if "has_service_workspace_access(user_id)" in current and "🔑 Оператор услуг" in current:
        return source, False
    return source[:start] + SHOW_MODE.rstrip() + "\n\n" + source[end:], True


def patch_language_gates_soft(source: str) -> tuple[str, bool]:
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
    if old_gate in source:
        return source.replace(old_gate, new_gate), True

    # Some current files use a multiline gate. Do not fail here:
    # service routing still works after language selection.
    return source, False


def find_after_lang_and_text(source: str, handler_start: int) -> int:
    """
    Find safe insertion point AFTER both:
      lang = user_languages.get(...)
      t = TEXTS[lang]

    This prevents NameError for `t` in service_global_switch.
    """
    lang_pos = source.find("    lang = user_languages.get(user_id, \"ru\")", handler_start)
    if lang_pos < 0:
        raise RuntimeError("Не найдена строка lang = user_languages.get(user_id, \"ru\") в message_handler().")

    t_pos = source.find("    t = TEXTS[lang]", lang_pos)
    if t_pos < 0:
        raise RuntimeError("Не найдена строка t = TEXTS[lang] после lang в message_handler().")

    end = source.find("\n", t_pos)
    if end < 0:
        raise RuntimeError("Не удалось определить конец строки t = TEXTS[lang].")
    return end + 1


def insert_service_active_route(source: str) -> tuple[str, bool]:
    if "# Операторский кабинет услуг" in source:
        return source, False

    handler_start = source.find("async def message_handler(")
    if handler_start < 0:
        raise RuntimeError("Не найдена async def message_handler().")

    pos = find_after_lang_and_text(source, handler_start)
    return source[:pos] + SERVICE_ACTIVE_ROUTE + source[pos:], True


def insert_service_general_route(source: str) -> tuple[str, bool]:
    if "# Заказы услуг: житель и оператор" in source:
        return source, False

    markers = [
        (
            "    # =========================\n"
            "    # Клиентский кабинет / заявки на пульты\n"
            "    # =========================\n"
        ),
        (
            "    # =========================\n"
            "    # Клиентский кабинет\n"
            "    # =========================\n"
        ),
    ]

    for marker in markers:
        if marker in source:
            return source.replace(marker, SERVICE_GENERAL_ROUTE + marker, 1), True

    call = "    if await handle_client_portal_text("
    pos = source.find(call)
    if pos >= 0:
        return source[:pos] + SERVICE_GENERAL_ROUTE + source[pos:], True

    raise RuntimeError("Не найден клиентский router или handle_client_portal_text для вставки service route.")


def insert_service_mode_switch(source: str) -> tuple[str, bool]:
    if 'if text in {"🔑 Оператор услуг", "🔑 Оператор послуг", "🔑 Service operator"}:' in source:
        return source, False
    if 'if text == "🔑 Оператор услуг":' in source:
        return source, False

    guard_marker = '    if text == "🛡 Пост охраны O":\n'
    if guard_marker in source:
        return source.replace(guard_marker, SERVICE_MODE_SWITCH + guard_marker, 1), True

    switch_marker = '    if text in {"🔄 Сменить режим", "🔄 Змінити режим", "🔄 Switch mode"}:\n'
    if switch_marker in source:
        return source.replace(switch_marker, SERVICE_MODE_SWITCH + switch_marker, 1), True

    raise RuntimeError("Не найдена точка вставки выбора режима оператора услуг.")


def patch(source: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    operations = [
        (add_service_import, "service workspace import"),
        (swap_client_portal_to_v3, "client_portal_v3 import"),
        (patch_show_mode_menu, "mode menu service operator button"),
        (patch_language_gates_soft, "language gate service access"),
        (insert_service_active_route, "service active route after lang/t"),
        (insert_service_general_route, "service general route"),
        (insert_service_mode_switch, "service operator mode switch"),
    ]

    for fn, label in operations:
        source, changed = fn(source)
        if changed:
            changes.append(label)

    required = [
        "from handlers.service_orders_workspace import (",
        "from handlers.client_portal_v3 import (",
        "handle_service_orders_text(",
        "has_service_workspace_access(user_id)",
        "show_service_operator_workspace(",
        "Заказы услуг: житель и оператор",
    ]
    missing = [item for item in required if item not in source]
    if missing:
        raise RuntimeError("Патч собран не полностью: " + ", ".join(missing))

    # Guard against the old bug: service block must be after t = TEXTS[lang].
    handler_start = source.find("async def message_handler(")
    block_pos = source.find("# Операторский кабинет услуг", handler_start)
    t_pos = source.find("    t = TEXTS[lang]", handler_start)
    if block_pos < 0 or t_pos < 0 or block_pos < t_pos:
        raise RuntimeError("Service active route вставлен до t = TEXTS[lang]. Это небезопасно.")

    compile(source, str(BOT_FILE), "exec")
    return source, changes


def write_report(
    original: str,
    patched: str,
    changes: list[str],
    dry_run: bool,
    backup: Path | None,
    preview: Path,
    diff_path: Path,
    report_path: Path,
) -> None:
    lines = []
    lines.append("# Service Orders UI v2 patch report")
    lines.append("")
    lines.append(f"Generated: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
    lines.append(f"Dry run: `{dry_run}`")
    lines.append(f"Bot: `{BOT_FILE}`")
    lines.append("")
    lines.append("## Changes")
    lines.append("")
    if changes:
        for c in changes:
            lines.append(f"- {c}")
    else:
        lines.append("- already patched")
    lines.append("")
    if backup:
        lines.append("## Backup")
        lines.append("")
        lines.append(f"`{backup}`")
        lines.append("")
    lines.append("## Preview")
    lines.append("")
    lines.append(f"`{preview}`")
    lines.append("")
    lines.append("## Diff")
    lines.append("")
    lines.append(f"`{diff_path}`")
    lines.append("")
    lines.append("## Required markers")
    lines.append("")
    markers = [
        "from handlers.service_orders_workspace import (",
        "from handlers.client_portal_v3 import (",
        "handle_service_orders_text(",
        "show_service_operator_workspace(",
        "🔑 Оператор услуг",
        "Заказы услуг: житель и оператор",
        "Операторский кабинет услуг",
    ]
    for marker in markers:
        lines.append(f"- {'OK' if marker in patched else 'MISSING'} `{marker}`")
    lines.append("")
    lines.append("## Safety check")
    lines.append("")
    handler_start = patched.find("async def message_handler(")
    t_pos = patched.find("    t = TEXTS[lang]", handler_start)
    block_pos = patched.find("# Операторский кабинет услуг", handler_start)
    lines.append(f"- `t = TEXTS[lang]` position: `{t_pos}`")
    lines.append(f"- service active block position: `{block_pos}`")
    lines.append(f"- service block after t: `{block_pos > t_pos}`")
    lines.append("")
    write_text(report_path, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    print("=" * 100)
    print("PATCH PARKING BOT: SERVICE ORDERS UI V2")
    print("=" * 100)
    print("Apply:", args.apply)

    for path in (BOT_FILE, WORKSPACE_FILE, PORTAL_FILE):
        if not path.exists():
            print("Missing:", path)
            return 1

    RECOVERED_DIR.mkdir(parents=True, exist_ok=True)
    ts = stamp()
    preview = RECOVERED_DIR / f"parking_bot_service_orders_ui_v2_{ts}.patched.py"
    diff_path = RECOVERED_DIR / f"parking_bot_service_orders_ui_v2_{ts}.diff"
    report_path = RECOVERED_DIR / f"parking_bot_service_orders_ui_v2_{ts}.md"

    original = read_text(BOT_FILE)

    try:
        patched, changes = patch(original)
    except Exception as exc:
        print("Patch check FAILED:", exc)
        return 1

    write_text(preview, patched)
    diff = difflib.unified_diff(
        original.splitlines(),
        patched.splitlines(),
        fromfile=str(BOT_FILE),
        tofile=str(preview),
        lineterm="",
    )
    write_text(diff_path, "\n".join(diff) + "\n")

    print("Changes:", "; ".join(changes or ["already patched"]))
    print("Changes needed:", patched != original)
    print("Preview:", preview)
    print("Diff:", diff_path)

    backup = None
    if args.apply and patched != original:
        backup_dir = ROOT / "Data" / "backups" / "source_code" / f"before_service_orders_ui_v2_{ts}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup = backup_dir / "parking_bot.py"
        shutil.copy2(BOT_FILE, backup)
        write_text(BOT_FILE, patched)
        compile(read_text(BOT_FILE), str(BOT_FILE), "exec")
        print("Backup:", backup)
        print("APPLIED")

    write_report(original, patched, changes, not args.apply, backup, preview, diff_path, report_path)
    print("Report:", report_path)

    if not args.apply:
        print("DRY RUN COMPLETED - NO FILES CHANGED")
        print("To apply:")
        print("python .\\OSBB\\patch_parking_bot_service_orders_ui_v2.py --apply")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
