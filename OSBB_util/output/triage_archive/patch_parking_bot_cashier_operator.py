"""
Подключает операторский кассовый редактор к существующему parking_bot.py.

Добавляет:
1) импорт handlers.cashier_operator;
2) кнопку 💰 Касса в ADMIN_MENU;
3) вызов handle_cashier_operator_text(...) до обычной навигации.

Не заменяет parking_bot.py целиком. Перед --apply создаёт backup.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import argparse
import shutil


ROOT = Path(__file__).resolve().parent
BOT_FILE = ROOT / "Bots" / "parking_bot.py"
HANDLER_FILE = ROOT / "Bots" / "handlers" / "cashier_operator.py"

IMPORT_LINE = "from handlers.cashier_operator import handle_cashier_operator_text\n"
CASHIER_BUTTON = "💰 Касса"

ROUTER_BLOCK = """    # =========================
    # Операторский кассовый редактор
    # =========================
    # O — основная касса охраны; K1..K6 — отдельные точки консьержей.
    # Обработчик вызывается до старого router состояний.
    if await handle_cashier_operator_text(
        update,
        user_states,
        user_id,
        text,
        is_admin=is_admin_user(user_id),
    ):
        return

"""


def backup_name(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return path.with_name(f"{path.stem}_before_cashier_editor_{stamp}{path.suffix}")


def find_matching_bracket(source: str, start: int) -> int:
    depth = 0
    in_single = False
    in_double = False
    escaped = False

    for idx in range(start, len(source)):
        char = source[idx]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "'" and not in_double:
            in_single = not in_single
            continue
        if char == '"' and not in_single:
            in_double = not in_double
            continue
        if in_single or in_double:
            continue

        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return idx

    raise RuntimeError("Не удалось найти конец ADMIN_MENU.")


def patch_import(source: str) -> tuple[str, bool]:
    if "from handlers.cashier_operator import handle_cashier_operator_text" in source:
        return source, False

    preferred = [
        "from handlers.client_portal import",
        "from handlers.audit_viewer import handle_audit_viewer_text\n",
        "from handlers.vehicle_full_list import handle_vehicle_full_list_text\n",
    ]

    # Multi-line import client_portal: add cashier after closing ).
    client_start = source.find("from handlers.client_portal import")
    if client_start >= 0:
        close = source.find(")\n", client_start)
        if close >= 0:
            close += 2
            return source[:close] + IMPORT_LINE + source[close:], True

    for marker in preferred[1:]:
        if marker in source:
            return source.replace(marker, marker + IMPORT_LINE, 1), True

    lines = source.splitlines(keepends=True)
    positions = [
        idx
        for idx, line in enumerate(lines)
        if line.startswith("from handlers.") or line.startswith("import handlers.")
    ]
    if not positions:
        raise RuntimeError("Не найдено место для импорта cashier_operator.")
    lines.insert(positions[-1] + 1, IMPORT_LINE)
    return "".join(lines), True


def patch_admin_menu(source: str) -> tuple[str, bool]:
    if CASHIER_BUTTON in source:
        return source, False

    marker = "ADMIN_MENU = ["
    pos = source.find(marker)
    if pos < 0:
        raise RuntimeError("Не найден ADMIN_MENU.")

    start = source.find("[", pos)
    end = find_matching_bracket(source, start)
    block = source[start:end + 1]
    lines = block.splitlines()
    lines.insert(-1, f'    ["{CASHIER_BUTTON}"],')
    new_block = "\n".join(lines)
    return source[:start] + new_block + source[end + 1:], True


def patch_router(source: str) -> tuple[str, bool]:
    if "handle_cashier_operator_text(" in source:
        return source, False

    marker = (
        "    # =========================\n"
        "    # Навигация\n"
        "    # =========================\n"
    )
    if marker not in source:
        raise RuntimeError(
            "Не найден раздел «Навигация» в message_handler. "
            "Исходный файл не изменён."
        )

    return source.replace(marker, ROUTER_BLOCK + marker, 1), True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    print("=" * 100)
    print("PATCH PARKING BOT: CASHIER OPERATOR")
    print("=" * 100)
    print("Bot:", BOT_FILE)
    print("Handler:", HANDLER_FILE)
    print("Apply:", args.apply)

    if not BOT_FILE.exists():
        raise SystemExit(f"Не найден parking_bot.py: {BOT_FILE}")
    if not HANDLER_FILE.exists():
        raise SystemExit(
            "Не найден Bots/handlers/cashier_operator.py. "
            "Сначала скопируйте handler."
        )

    original = BOT_FILE.read_text(encoding="utf-8")
    patched = original

    patched, import_added = patch_import(patched)
    patched, menu_added = patch_admin_menu(patched)
    patched, router_added = patch_router(patched)

    try:
        compile(patched, str(BOT_FILE), "exec")
    except SyntaxError as exc:
        raise SystemExit(
            f"После patcher код не компилируется: {exc}\n"
            "Исходный файл не изменён."
        )

    print("Import added:", import_added)
    print("Admin button added:", menu_added)
    print("Router added:", router_added)
    print("Changes needed:", patched != original)

    if not args.apply:
        print()
        print("DRY RUN COMPLETED - NO CHANGES SAVED")
        return

    if patched == original:
        print()
        print("ALREADY PATCHED - NO FILE CHANGE")
        return

    backup = backup_name(BOT_FILE)
    shutil.copy2(BOT_FILE, backup)
    BOT_FILE.write_text(patched, encoding="utf-8")

    print("Backup:", backup)
    print("APPLIED")


if __name__ == "__main__":
    main()
