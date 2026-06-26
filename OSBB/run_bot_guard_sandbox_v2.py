"""
Запуск Telegram-бота с отдельной guard sandbox-копией БД.

Использует:
- обычный Telegram token;
- исходный parking_bot.py только для чтения;
- v2-переключение и guard patch только в памяти;
- указанную .db исключительно из Data/db/sandbox.

Не изменяет config.py и не сохраняет патч в parking_bot.py.

Перед --run обязательно остановите обычный бот, иначе Telegram getUpdates
будет конфликтовать между двумя экземплярами.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import os
import sqlite3
import sys
import traceback
from pathlib import Path
from types import SimpleNamespace
from typing import Any


ROOT = Path(__file__).resolve().parent
BOTS = ROOT / "Bots"
SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
BOT_FILE = BOTS / "parking_bot.py"
V2_SWITCHER = ROOT / "switch_parking_bot_to_cashier_v2.py"
GUARD_PATCHER = ROOT / "patch_parking_bot_guard_workspace_v3.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Не удалось подготовить модуль: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def inside_sandbox(path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(SANDBOX_DIR.resolve())
    except ValueError as exc:
        raise ValueError(
            "Для запуска разрешены только .db внутри Data\\db\\sandbox."
        ) from exc
    return resolved


def clone_paths(original: Any, sandbox_db: Path):
    try:
        cloned = copy.copy(original)
        if cloned is original:
            raise RuntimeError
    except Exception:
        data = {}
        for name in dir(original):
            if name.startswith("_"):
                continue
            value = getattr(original, name)
            if not callable(value):
                data[name] = value
        cloned = SimpleNamespace(**data)
    try:
        setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
    except Exception:
        object.__setattr__(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
    return cloned


def configure_sandbox(sandbox_db: Path) -> None:
    for folder in (ROOT, BOTS, ROOT.parent):
        if str(folder) not in sys.path:
            sys.path.insert(0, str(folder))

    import config

    original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
    original_prod = Path(config.paths.OSBB_DB_FILE).resolve()
    if sandbox_db == original_test or sandbox_db == original_prod:
        raise RuntimeError("Отказ: указан путь рабочей БД, а не sandbox-копии.")

    config.paths = clone_paths(config.paths, sandbox_db)
    config.USE_TEST_DB = True
    os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
    os.environ["OSBB_SANDBOX_MODE"] = "1"


def table_rows(sandbox_db: Path) -> dict[str, int]:
    tables = [
        "staff_principals",
        "access_user_roles",
        "access_user_permissions",
        "access_audit_log",
        "payment_notices",
        "cashier_receipts",
        "remote_requests",
        "remote_handover_events",
    ]
    conn = sqlite3.connect(sandbox_db)
    try:
        cur = conn.cursor()
        result = {}
        for table in tables:
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


def patched_source() -> tuple[str, list[str], list[str]]:
    if not BOT_FILE.exists():
        raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
    if not V2_SWITCHER.exists():
        raise FileNotFoundError(f"Не найден v2 switcher: {V2_SWITCHER}")
    if not GUARD_PATCHER.exists():
        raise FileNotFoundError(f"Не найден guard patcher: {GUARD_PATCHER}")

    v2 = load_module(V2_SWITCHER, "_sandbox_v2_switcher")
    guard = load_module(GUARD_PATCHER, "_sandbox_guard_patcher")

    source = BOT_FILE.read_text(encoding="utf-8")
    source, v2_changes = v2.patch(source)
    source, guard_changes = guard.patch(source)
    compile(source, str(BOT_FILE), "exec")
    return source, v2_changes, guard_changes


def run_bot(source: str) -> None:
    os.chdir(BOTS)

    # Do not reuse potentially live-bound project modules.
    for name in list(sys.modules):
        if name in {
            "cashier_v2_core",
            "access_control",
            "audit_logger",
            "db_access",
            "Bots.db_access",
            "handlers.client_portal",
            "handlers.client_portal_v2",
            "handlers.cashier_operator",
            "handlers.cashier_operator_v2",
            "handlers.guard_workspace",
        }:
            sys.modules.pop(name, None)

    namespace = {
        "__name__": "__main__",
        "__file__": str(BOT_FILE),
        "__package__": None,
    }
    exec(compile(source, str(BOT_FILE), "exec"), namespace)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sandbox", required=True)
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    sandbox_db = inside_sandbox(Path(args.sandbox))
    if not sandbox_db.exists():
        raise SystemExit(f"Не найдена sandbox-БД: {sandbox_db}")

    print("=" * 100)
    print("OSBB GUARD SANDBOX BOT V2")
    print("=" * 100)
    print("Sandbox DB:", sandbox_db)
    print("Mode:", "RUN TELEGRAM BOT" if args.run else "CHECK ONLY")

    try:
        summary = table_rows(sandbox_db)
        missing = [name for name, count in summary.items() if count < 0]
        if missing:
            raise RuntimeError(
                "Sandbox не подготовлен для кабинета охраны. Нет таблиц: "
                + ", ".join(missing)
            )

        print()
        print("Sandbox rows:")
        for name, count in summary.items():
            print(f"  {name}: {count}")

        configure_sandbox(sandbox_db)
        source, v2_changes, guard_changes = patched_source()
        print()
        print("Runtime patches:")
        print("  v2:", "; ".join(v2_changes))
        print("  guard:", "; ".join(guard_changes))

        if not args.run:
            print()
            print("CHECK PASSED")
            print("Telegram polling was NOT started.")
            print("No DB/source/config files were changed.")
            return 0

        print()
        print("Before proceeding confirm ordinary bot is stopped.")
        print("All test records will be written only to:", sandbox_db)
        print("Stop this sandbox bot with Ctrl+C.")
        print()
        run_bot(source)
        return 0

    except KeyboardInterrupt:
        print("\nGuard sandbox bot stopped by Ctrl+C.")
        return 0
    except Exception:
        print("\nGUARD SANDBOX LAUNCH FAILED")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
