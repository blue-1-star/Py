r"""
Запуск изолированной live sandbox с кабинетами:
- житель: «Пульты и доступ»;
- пост охраны O;
- оператор услуг пультов и телефонного доступа.

Все изменения Bots/parking_bot.py выполняются только в памяти текущего процесса.
Работает исключительно с указанной .db внутри Data\db\sandbox.
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
GUARD_PATCHER = ROOT / "patch_parking_bot_guard_workspace_v4.py"
SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_ui_v1.py"
SERVICE_CORE = ROOT / "service_orders_core.py"


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
    setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
    return cloned


def configure_sandbox(sandbox_db: Path) -> None:
    for folder in (ROOT, BOTS, ROOT.parent):
        if str(folder) not in sys.path:
            sys.path.insert(0, str(folder))

    import config

    original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
    original_prod = Path(config.paths.OSBB_DB_FILE).resolve()
    if sandbox_db in {original_test, original_prod}:
        raise RuntimeError("Отказ: указан путь рабочей базы, а не sandbox-копии.")

    config.paths = clone_paths(config.paths, sandbox_db)
    config.USE_TEST_DB = True
    os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
    os.environ["OSBB_SANDBOX_MODE"] = "1"


def table_rows(sandbox_db: Path) -> dict[str, int]:
    names = [
        "staff_principals",
        "access_user_roles",
        "payment_notices",
        "cashier_receipts",
        "service_orders",
        "service_order_steps",
        "service_order_payment_links",
        "remote_assets",
        "remote_asset_movements",
        "service_access_credentials",
        "service_item_workflows",
    ]
    conn = sqlite3.connect(sandbox_db)
    try:
        cur = conn.cursor()
        result = {}
        for name in names:
            cur.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
                (name,),
            )
            if cur.fetchone() is None:
                result[name] = -1
            else:
                cur.execute(f'SELECT COUNT(*) FROM "{name}"')
                result[name] = int(cur.fetchone()[0] or 0)
        return result
    finally:
        conn.close()


def required_files() -> list[Path]:
    return [
        BOT_FILE,
        V2_SWITCHER,
        GUARD_PATCHER,
        SERVICE_PATCHER,
        SERVICE_CORE,
        BOTS / "handlers" / "guard_workspace.py",
        BOTS / "handlers" / "client_portal_v3.py",
        BOTS / "handlers" / "service_orders_workspace.py",
    ]


def patched_source() -> tuple[str, list[str], list[str], list[str]]:
    missing = [str(path) for path in required_files() if not path.exists()]
    if missing:
        raise FileNotFoundError("Не найдены файлы:\n" + "\n".join(missing))

    if "# SAFE_PAYMENT_LINK_POLICY_V1" not in SERVICE_CORE.read_text(encoding="utf-8"):
        raise RuntimeError(
            "Не установлена безопасная политика привязки оплаты. "
            "Сначала выполните install_service_orders_ui.py --apply."
        )

    v2 = load_module(V2_SWITCHER, "_live_service_v2_switcher")
    guard = load_module(GUARD_PATCHER, "_live_service_guard_patcher")
    service = load_module(SERVICE_PATCHER, "_live_service_ui_patcher")

    source = BOT_FILE.read_text(encoding="utf-8")
    source, v2_changes = v2.patch(source)
    source, guard_changes = guard.patch(source)
    source, service_changes = service.patch(source)
    compile(source, str(BOT_FILE), "exec")
    return source, v2_changes, guard_changes, service_changes


def run_bot(source: str) -> None:
    os.chdir(BOTS)

    for name in list(sys.modules):
        if name in {
            "cashier_v2_core",
            "service_orders_core",
            "service_catalog_admin_core",
            "access_control",
            "audit_logger",
            "db_access",
            "Bots.db_access",
            "handlers.client_portal",
            "handlers.client_portal_v2",
            "handlers.client_portal_v3",
            "handlers.cashier_operator",
            "handlers.cashier_operator_v2",
            "handlers.guard_workspace",
            "handlers.service_orders_workspace",
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
    print("OSBB LIVE SERVICE SANDBOX BOT V4")
    print("=" * 100)
    print("Sandbox DB:", sandbox_db)
    print("Mode:", "RUN TELEGRAM BOT" if args.run else "CHECK ONLY")

    try:
        summary = table_rows(sandbox_db)
        missing = [name for name, count in summary.items() if count < 0]
        if missing:
            raise RuntimeError(
                "Sandbox не подготовлен для услуг/пультов. Нет таблиц: "
                + ", ".join(missing)
            )

        print("\nSandbox rows:")
        for name, count in summary.items():
            print(f"  {name}: {count}")

        configure_sandbox(sandbox_db)
        source, v2_changes, guard_changes, service_changes = patched_source()
        print("\nRuntime patches:")
        print("  v2:", "; ".join(v2_changes))
        print("  guard:", "; ".join(guard_changes))
        print("  services:", "; ".join(service_changes))

        if not args.run:
            print("\nCHECK PASSED")
            print("Telegram polling was NOT started.")
            print("No database, config.py or parking_bot.py was changed.")
            return 0

        print("\nBefore proceeding confirm that every other Telegram bot instance is stopped.")
        print("All new records will be written only to:", sandbox_db)
        print("Stop this sandbox bot with Ctrl+C.\n")
        run_bot(source)
        return 0

    except KeyboardInterrupt:
        print("\nLive service sandbox bot stopped by Ctrl+C.")
        return 0
    except Exception:
        print("\nLIVE SERVICE SANDBOX LAUNCH FAILED")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
