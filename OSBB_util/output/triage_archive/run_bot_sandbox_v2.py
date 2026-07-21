r"""
Безопасный запуск Telegram-бота с sandbox-копией БД и кассой v2.

Этот файл НЕ:
- изменяет config.py;
- заменяет рабочий Bots/parking_bot.py;
- изменяет osbb_test.db или osbb.db.

Он запускает parking_bot.py только в памяти:
- подменяет путь TEST-БД на явно заданную копию из Data/db/sandbox;
- подменяет импорты client_portal/cashier_operator на v2 только в памяти;
- использует обычный Telegram token.

ВАЖНО:
Перед --run остановите обычный бот. Два экземпляра с одним токеном
нельзя запускать одновременно: Telegram будет отдавать обновления только
одному из них или покажет конфликт getUpdates.

Сначала проверить без запуска:
  g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\run_bot_sandbox_v2.py ^
    --sandbox "G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09.db"

Запустить Telegram-бот на копии БД:
  g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\run_bot_sandbox_v2.py ^
    --sandbox "G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09.db" ^
    --run
"""

from __future__ import annotations

import argparse
import copy
import os
import sqlite3
import sys
import traceback
from pathlib import Path
from types import SimpleNamespace
from typing import Any


ROOT = Path(__file__).resolve().parent
BOTS_DIR = ROOT / "Bots"
SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
BOT_FILE = BOTS_DIR / "parking_bot.py"
SWITCHER_FILE = ROOT / "switch_parking_bot_to_cashier_v2.py"


def load_module(path: Path, module_name: str):
    import importlib.util

    spec = importlib.util.spec_from_file_location(module_name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Не удалось подготовить модуль: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ensure_inside_sandbox(path: Path) -> Path:
    resolved = path.resolve()
    sandbox = SANDBOX_DIR.resolve()
    try:
        resolved.relative_to(sandbox)
    except ValueError as exc:
        raise ValueError(
            "Разрешены только базы внутри папки Data\\db\\sandbox.\n"
            f"Передан путь: {resolved}\n"
            f"Разрешённая папка: {sandbox}"
        ) from exc
    return resolved


def clone_paths_with_sandbox(original_paths: Any, sandbox_db: Path):
    """
    Создаёт отдельный объект paths для текущего процесса.
    Оригинальный config.paths и config.py на диске не меняются.
    """
    try:
        cloned = copy.copy(original_paths)
        if cloned is original_paths:
            raise RuntimeError("copy returned same object")
    except Exception:
        values = {}
        for name in dir(original_paths):
            if name.startswith("_"):
                continue
            try:
                value = getattr(original_paths, name)
            except Exception:
                continue
            if not callable(value):
                values[name] = value
        cloned = SimpleNamespace(**values)

    try:
        setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
    except Exception:
        # Supports a frozen dataclass copy.
        object.__setattr__(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
    return cloned


def sqlite_summary(path: Path) -> dict[str, int]:
    required = [
        "payment_notices",
        "bank_transactions",
        "cashier_batches",
        "cashier_batch_items",
        "cashier_reconciliation_cases",
        "cashier_receipts",
        "payments",
    ]
    conn = sqlite3.connect(path)
    try:
        cur = conn.cursor()
        result: dict[str, int] = {}
        for table in required:
            cur.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
                (table,),
            )
            if cur.fetchone() is None:
                result[table] = -1
            else:
                cur.execute(f'SELECT COUNT(*) FROM "{table}"')
                result[table] = int(cur.fetchone()[0] or 0)
        return result
    finally:
        conn.close()


def same_path(left: Path, right: Path) -> bool:
    try:
        return left.resolve() == right.resolve()
    except Exception:
        return str(left).lower() == str(right).lower()


def configure_runtime_database(sandbox_db: Path) -> None:
    """
    Must run before importing parking_bot.py and its project modules.
    """
    for path in (ROOT, BOTS_DIR, ROOT.parent):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))

    import config

    original_test = Path(config.paths.OSBB_TEST_DB_FILE)
    original_prod = Path(config.paths.OSBB_DB_FILE)

    if same_path(sandbox_db, original_test) or same_path(sandbox_db, original_prod):
        raise RuntimeError(
            "Отказ: передана рабочая БД, а не sandbox-копия."
        )

    config.paths = clone_paths_with_sandbox(config.paths, sandbox_db)
    config.USE_TEST_DB = True

    # Extra diagnostic marker for any future code that wants to inspect it.
    os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
    os.environ["OSBB_SANDBOX_MODE"] = "1"


def patched_bot_source() -> tuple[str, list[str]]:
    if not BOT_FILE.exists():
        raise FileNotFoundError(f"Не найден бот: {BOT_FILE}")
    if not SWITCHER_FILE.exists():
        raise FileNotFoundError(f"Не найден переключатель v2: {SWITCHER_FILE}")

    switcher = load_module(SWITCHER_FILE, "_osbb_sandbox_switcher")
    source = BOT_FILE.read_text(encoding="utf-8")
    patched, changes = switcher.patch(source)
    compile(patched, str(BOT_FILE), "exec")
    return patched, changes


def run_bot_in_memory(source: str) -> None:
    """
    parking_bot.py executed from its true path, but only the patched source
    is used for this process. No file write occurs.
    """
    os.chdir(BOTS_DIR)

    # Ensure a prior accidental project import cannot retain the real DB object.
    for module_name in list(sys.modules):
        if module_name in {
            "Bots.db_access",
            "db_access",
            "handlers.client_portal",
            "handlers.client_portal_v2",
            "handlers.cashier_operator",
            "handlers.cashier_operator_v2",
            "cashier_v2_core",
            "audit_logger",
        }:
            sys.modules.pop(module_name, None)

    namespace = {
        "__name__": "__main__",
        "__file__": str(BOT_FILE),
        "__package__": None,
    }
    exec(compile(source, str(BOT_FILE), "exec"), namespace)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run OSBB bot v2 with a sandbox database only."
    )
    parser.add_argument(
        "--sandbox",
        required=True,
        help="Absolute path to a .db file inside Data\\db\\sandbox",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Actually start Telegram polling. Without this flag only checks are made.",
    )
    args = parser.parse_args()

    sandbox_db = ensure_inside_sandbox(Path(args.sandbox))
    if not sandbox_db.exists():
        raise SystemExit(f"Не найдена sandbox-копия БД: {sandbox_db}")

    print("=" * 100)
    print("OSBB SANDBOX BOT V2")
    print("=" * 100)
    print("Project:", ROOT)
    print("Sandbox DB:", sandbox_db)
    print("Live bot file (read only):", BOT_FILE)
    print("Mode:", "RUN TELEGRAM BOT" if args.run else "CHECK ONLY")
    print()

    try:
        summary = sqlite_summary(sandbox_db)
        missing = [table for table, count in summary.items() if count < 0]
        if missing:
            raise RuntimeError(
                "Sandbox-копия не содержит таблицы v2: " + ", ".join(missing)
            )

        print("Sandbox DB tables:")
        for table, count in summary.items():
            print(f"  {table}: {count} rows")

        configure_runtime_database(sandbox_db)
        source, changes = patched_bot_source()

        print()
        print("Runtime patch:")
        for item in changes:
            print("  -", item)

        if not args.run:
            print()
            print("CHECK PASSED")
            print("No database and no bot source files were changed.")
            print("Telegram polling was NOT started.")
            return 0

        print()
        print("ATTENTION")
        print("1. Make sure the ordinary production/test bot is stopped.")
        print("2. This process uses the normal Telegram token but writes only to:")
        print("   ", sandbox_db)
        print("3. Stop sandbox bot with Ctrl+C when testing is finished.")
        print()
        print("Starting sandbox bot...")
        run_bot_in_memory(source)
        return 0

    except KeyboardInterrupt:
        print("\nSandbox bot stopped by Ctrl+C.")
        return 0
    except Exception:
        print("\nSANDBOX LAUNCH FAILED")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
