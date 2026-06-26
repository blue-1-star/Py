"""
Безопасно подключает client_cabinet.py к существующему Bots/parking_bot.py.

Почему отдельный patcher:
- рабочий parking_bot.py уже содержит добавленные ранее модули;
- этот скрипт не заменяет его старой копией;
- он делает резервную копию и добавляет ровно две вставки:
  1) import handlers.client_cabinet
  2) вызов handle_client_cabinet_text(...) до общего router состояний.

Запуск:
  g:/Programming/Py/venv/Scripts/python.exe G:/Programming/Py/OSBB/patch_parking_bot_client_cabinet.py
  g:/Programming/Py/venv/Scripts/python.exe G:/Programming/Py/OSBB/patch_parking_bot_client_cabinet.py --apply
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import argparse
import shutil


OSBB_ROOT = Path(__file__).resolve().parent
BOT_FILE = OSBB_ROOT / "Bots" / "parking_bot.py"
HANDLER_FILE = OSBB_ROOT / "Bots" / "handlers" / "client_cabinet.py"

IMPORT_LINE = (
    "from handlers.client_cabinet import handle_client_cabinet_text\n"
)

ROUTER_BLOCK = """
    # =========================
    # Клиентский кабинет
    # =========================
    # Обрабатывает личный кабинет, парковочный счёт и честные заглушки
    # до общего state-router. В admin-режиме обработчик не перехватывает
    # операторские сценарии.
    if await handle_client_cabinet_text(
        update,
        user_states,
        user_id,
        text,
        user_mode=user_modes.get(user_id),
    ):
        return

"""


def backup_name(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return path.with_name(f"{path.stem}_before_client_cabinet_{stamp}{path.suffix}")


def insert_import(source: str) -> tuple[str, bool]:
    if "from handlers.client_cabinet import handle_client_cabinet_text" in source:
        return source, False

    marker_candidates = [
        "from handlers.audit_viewer import handle_audit_viewer_text\n",
        "from handlers.vehicle_full_list import handle_vehicle_full_list_text\n",
        "from handlers.vehicle_card_editor import handle_vehicle_card_editor_text\n",
    ]

    for marker in marker_candidates:
        if marker in source:
            return source.replace(marker, marker + IMPORT_LINE, 1), True

    lines = source.splitlines(keepends=True)
    positions = [
        index
        for index, line in enumerate(lines)
        if line.startswith("from handlers.") or line.startswith("import handlers.")
    ]
    if positions:
        pos = positions[-1] + 1
        lines.insert(pos, IMPORT_LINE)
        return "".join(lines), True

    raise RuntimeError(
        "Не найдено безопасное место для import handlers.client_cabinet."
    )


def insert_router(source: str) -> tuple[str, bool]:
    if "handle_client_cabinet_text(" in source:
        return source, False

    marker = (
        '    # =========================\n'
        '    # Состояния пользователя\n'
        '    # =========================\n'
    )

    if marker not in source:
        raise RuntimeError(
            "Не найден раздел «Состояния пользователя» в parking_bot.py. "
            "Изменений не внесено."
        )

    return source.replace(marker, ROUTER_BLOCK + marker, 1), True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    print("=" * 100)
    print("PATCH PARKING BOT: CLIENT CABINET")
    print("=" * 100)
    print("Bot file:", BOT_FILE)
    print("Handler file:", HANDLER_FILE)
    print("Apply:", args.apply)

    if not BOT_FILE.exists():
        raise SystemExit(f"Не найден файл бота: {BOT_FILE}")
    if not HANDLER_FILE.exists():
        raise SystemExit(
            "Не найден client_cabinet.py. "
            "Сначала положите его в Bots/handlers."
        )

    source = BOT_FILE.read_text(encoding="utf-8")
    original = source

    source, import_added = insert_import(source)
    source, router_added = insert_router(source)

    try:
        compile(source, str(BOT_FILE), "exec")
    except SyntaxError as exc:
        raise SystemExit(
            f"После patcher получился синтаксический конфликт: {exc}\n"
            "Исходный parking_bot.py не изменён."
        )

    print("Import added:", import_added)
    print("Router added:", router_added)
    print("Changes needed:", source != original)

    if not args.apply:
        print()
        print("DRY RUN COMPLETED - NO CHANGES SAVED")
        return

    if source == original:
        print()
        print("ALREADY PATCHED - NO FILE CHANGE")
        return

    backup = backup_name(BOT_FILE)
    shutil.copy2(BOT_FILE, backup)
    BOT_FILE.write_text(source, encoding="utf-8")

    print("Backup:", backup)
    print("APPLIED")


if __name__ == "__main__":
    main()
