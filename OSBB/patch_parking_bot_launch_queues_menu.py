"""
Добавляет в admin-меню две рабочие очереди запуска:
- 🔑 Заявки на пульты
- 🔗 Запросы квартир

Кнопки обрабатывает новый Bots/handlers/client_portal.py.
Patcher не меняет БД и делает backup parking_bot.py.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import argparse
import shutil


ROOT = Path(__file__).resolve().parent
BOT_FILE = ROOT / "Bots" / "parking_bot.py"
BUTTONS = ["🔑 Заявки на пульты", "🔗 Запросы квартир"]


def backup_name(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return path.with_name(f"{path.stem}_before_launch_queues_menu_{stamp}{path.suffix}")


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


def patch_admin_menu(source: str) -> tuple[str, list[str]]:
    marker = "ADMIN_MENU = ["
    start = source.find(marker)
    if start < 0:
        raise RuntimeError("Не найден ADMIN_MENU в parking_bot.py.")

    bracket_start = source.find("[", start)
    bracket_end = find_matching_bracket(source, bracket_start)
    block = source[bracket_start:bracket_end + 1]

    missing = [button for button in BUTTONS if button not in block]
    if not missing:
        return source, []

    lines = block.splitlines()
    for button in missing:
        lines.insert(-1, f'    ["{button}"],')

    patched_block = "\n".join(lines)
    return source[:bracket_start] + patched_block + source[bracket_end + 1:], missing


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if not BOT_FILE.exists():
        raise SystemExit(f"Не найден файл: {BOT_FILE}")

    original = BOT_FILE.read_text(encoding="utf-8")
    patched, missing = patch_admin_menu(original)

    try:
        compile(patched, str(BOT_FILE), "exec")
    except SyntaxError as exc:
        raise SystemExit(
            f"После добавления меню код не компилируется: {exc}\n"
            "Исходный файл не изменён."
        )

    print("=" * 96)
    print("PATCH ADMIN MENU: LAUNCH QUEUES")
    print("=" * 96)
    print("Bot:", BOT_FILE)
    print("Apply:", args.apply)
    print("Buttons to add:", ", ".join(missing) if missing else "none")
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
