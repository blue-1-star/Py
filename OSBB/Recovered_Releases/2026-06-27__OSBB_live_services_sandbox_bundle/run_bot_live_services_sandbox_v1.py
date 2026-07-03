# -*- coding: utf-8 -*-
"""
Launch the real service-order test workflow in the dedicated live-services
sandbox database.

This runner:
- uses only the known live-services sandbox database;
- switches the bot to cashier v2 in memory;
- connects service_orders_workspace to parking_bot in memory;
- uses the corrected full workspace file supplied with this bundle;
- prepares sandbox-only service permissions for test operators;
- never changes Bots\\parking_bot.py or config.py.

It is intentionally separate from the old Guard Sandbox runner.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import os
import shutil
import sqlite3
import subprocess
import sys
import traceback
from datetime import datetime
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any


ROOT = Path(__file__).resolve().parent
BOTS_DIR = ROOT / "Bots"
SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
BACKUP_DIR = SANDBOX_DIR / "backups"

LIVE_SERVICES_DB = (
    SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
)

BOT_FILE = BOTS_DIR / "parking_bot.py"
WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
V2_SWITCHER = ROOT / "switch_parking_bot_to_cashier_v2.py"
SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"

# 210312208 accepted the resident remote in SO-20260626-000001.
# Configured admins are added automatically as well.
KNOWN_TEST_OPERATOR_IDS = {210312208}
SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Не удалось загрузить модуль: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def clone_paths(original: Any, sandbox_db: Path) -> Any:
    try:
        cloned = copy.copy(original)
        if cloned is original:
            raise RuntimeError
    except Exception:
        values = {
            name: getattr(original, name)
            for name in dir(original)
            if not name.startswith("_") and not callable(getattr(original, name))
        }
        cloned = SimpleNamespace(**values)

    setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
    return cloned


def configure_sandbox(sandbox_db: Path) -> None:
    for folder in (ROOT, BOTS_DIR, ROOT.parent):
        if str(folder) not in sys.path:
            sys.path.insert(0, str(folder))

    import config

    original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
    original_prod = Path(config.paths.OSBB_DB_FILE).resolve()
    if sandbox_db.resolve() in {original_test, original_prod}:
        raise RuntimeError(
            "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
            "не основную базу и не штатную test-БД."
        )

    config.paths = clone_paths(config.paths, sandbox_db)
    config.USE_TEST_DB = True
    os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
    os.environ["OSBB_SANDBOX_MODE"] = "1"
    os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"

    if str(config.paths.SECRETS_DIR) not in sys.path:
        sys.path.insert(0, str(config.paths.SECRETS_DIR))


def tables(conn: sqlite3.Connection) -> set[str]:
    return {
        str(row[0])
        for row in conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            """
        ).fetchall()
    }


def columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    safe_name = str(table_name).replace('"', '""')
    return {
        str(row[1])
        for row in conn.execute(f'PRAGMA table_info("{safe_name}")').fetchall()
    }


def create_backup(db_path: Path, reason: str) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = BACKUP_DIR / f"{db_path.stem}_before_{reason}_{stamp}{db_path.suffix}"
    shutil.copy2(db_path, backup)
    return backup


def configured_operator_ids() -> list[int]:
    user_ids = set(KNOWN_TEST_OPERATOR_IDS)
    try:
        from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS

        for raw_id in tuple(ADMIN_IDS) + tuple(SUPER_ADMIN_IDS):
            try:
                user_ids.add(int(raw_id))
            except (TypeError, ValueError):
                pass
    except Exception as exc:
        print(f"WARNING: unable to read configured admin IDs: {exc}")

    return sorted(user_ids)


def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
    """
    Give configured test operators sandbox-only permissions for service orders.
    No order, payment or remote record is altered.
    """
    conn = sqlite3.connect(db_path)
    try:
        present = tables(conn)
        required = {"access_user_roles", "access_role_permissions"}
        missing = sorted(required - present)
        if missing:
            return [], [f"permissions not seeded: missing tables {', '.join(missing)}"], None

        user_role_columns = columns(conn, "access_user_roles")
        role_permission_columns = columns(conn, "access_role_permissions")
        expected_user_columns = {
            "telegram_user_id", "role_code", "scope_type", "scope_value",
            "is_active",
        }
        expected_permission_columns = {
            "role_code", "resource", "action", "scope_type", "scope_value",
            "effect", "is_active",
        }
        if not expected_user_columns.issubset(user_role_columns):
            return [], ["permissions not seeded: access_user_roles schema is incompatible"], None
        if not expected_permission_columns.issubset(role_permission_columns):
            return [], ["permissions not seeded: access_role_permissions schema is incompatible"], None

        requested_users = configured_operator_ids()
        role_permissions: list[tuple[str, str]] = [
            ("service_orders", "VIEW"),
            ("service_orders", "CREATE"),
            ("service_orders", "UPDATE"),
            ("service_orders", "CONFIRM"),
            ("service_order_steps", "VIEW"),
            ("service_order_steps", "CREATE"),
            ("service_order_steps", "CONFIRM"),
            ("service_order_payment_links", "VIEW"),
            ("service_order_payment_links", "CREATE"),
            ("remote_assets", "VIEW"),
            ("remote_assets", "CREATE"),
            ("remote_assets", "UPDATE"),
            ("remote_asset_movements", "VIEW"),
            ("remote_asset_movements", "CREATE"),
            ("access_credentials", "VIEW"),
            ("access_credentials", "CREATE"),
        ]
        changes: list[str] = []
        needs_change = False

        for user_id in requested_users:
            exists = conn.execute(
                """
                SELECT 1
                FROM access_user_roles
                WHERE telegram_user_id = ?
                  AND role_code = ?
                  AND scope_type = 'ALL'
                  AND scope_value = '*'
                  AND COALESCE(is_active, 1) = 1
                LIMIT 1
                """,
                (str(user_id), SANDBOX_SERVICE_ROLE),
            ).fetchone()
            if not exists:
                needs_change = True

        for resource, action in role_permissions:
            for category in ("REMOTE", "ACCESS"):
                exists = conn.execute(
                    """
                    SELECT 1
                    FROM access_role_permissions
                    WHERE role_code = ?
                      AND resource = ?
                      AND action = ?
                      AND scope_type = 'SERVICE_CATEGORY'
                      AND scope_value = ?
                      AND effect = 'ALLOW'
                      AND COALESCE(is_active, 1) = 1
                    LIMIT 1
                    """,
                    (SANDBOX_SERVICE_ROLE, resource, action, category),
                ).fetchone()
                if not exists:
                    needs_change = True

        backup: Path | None = None
        if needs_change:
            backup = create_backup(db_path, "service_operator_permissions")

            for user_id in requested_users:
                exists = conn.execute(
                    """
                    SELECT 1
                    FROM access_user_roles
                    WHERE telegram_user_id = ?
                      AND role_code = ?
                      AND scope_type = 'ALL'
                      AND scope_value = '*'
                      AND COALESCE(is_active, 1) = 1
                    LIMIT 1
                    """,
                    (str(user_id), SANDBOX_SERVICE_ROLE),
                ).fetchone()
                if not exists:
                    conn.execute(
                        """
                        INSERT INTO access_user_roles
                            (telegram_user_id, role_code, scope_type, scope_value,
                             is_active, note, created_at, updated_at)
                        VALUES (?, ?, 'ALL', '*', 1, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        """,
                        (
                            str(user_id),
                            SANDBOX_SERVICE_ROLE,
                            "Sandbox role for service-order workflow testing.",
                        ),
                    )
                    changes.append(f"role assigned to Telegram ID {user_id}")

            for resource, action in role_permissions:
                for category in ("REMOTE", "ACCESS"):
                    exists = conn.execute(
                        """
                        SELECT 1
                        FROM access_role_permissions
                        WHERE role_code = ?
                          AND resource = ?
                          AND action = ?
                          AND scope_type = 'SERVICE_CATEGORY'
                          AND scope_value = ?
                          AND effect = 'ALLOW'
                          AND COALESCE(is_active, 1) = 1
                        LIMIT 1
                        """,
                        (SANDBOX_SERVICE_ROLE, resource, action, category),
                    ).fetchone()
                    if not exists:
                        conn.execute(
                            """
                            INSERT INTO access_role_permissions
                                (role_code, resource, action, scope_type, scope_value,
                                 effect, is_active, note, created_at, updated_at)
                            VALUES (?, ?, ?, 'SERVICE_CATEGORY', ?, 'ALLOW', 1, ?,
                                    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                            """,
                            (
                                SANDBOX_SERVICE_ROLE,
                                resource,
                                action,
                                category,
                                "Sandbox-only service workflow permission.",
                            ),
                        )
                        changes.append(
                            f"permission {resource}/{action}/{category}"
                        )

            conn.commit()

        return requested_users, changes, backup
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def assert_workspace_is_compatible() -> None:
    if not WORKSPACE_FILE.is_file():
        raise FileNotFoundError(f"Не найден модуль услуг: {WORKSPACE_FILE}")

    source = WORKSPACE_FILE.read_text(encoding="utf-8")
    required = (
        "def _payments_columns(cur: sqlite3.Cursor)",
        "CAST(p.apartment_number AS TEXT)",
        "NULL AS source_ref",
    )
    missing = [marker for marker in required if marker not in source]
    if missing:
        raise RuntimeError(
            "В service_orders_workspace.py не установлена готовая совместимая "
            "версия. Не хватает: " + ", ".join(missing)
        )
    compile(source, str(WORKSPACE_FILE), "exec")


def purge_project_modules() -> None:
    exact_names = {
        "cashier_v2_core",
        "access_control",
        "audit_logger",
        "db_access",
        "Bots.db_access",
        "service_orders_core",
        "handlers.client_portal",
        "handlers.client_portal_v2",
        "handlers.cashier_operator",
        "handlers.cashier_operator_v2",
        "handlers.service_orders_workspace",
        "handlers.guard_workspace",
    }
    for name in list(sys.modules):
        if name in exact_names:
            sys.modules.pop(name, None)


def patch_bot_source() -> tuple[str, list[str]]:
    if not BOT_FILE.is_file():
        raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
    if not V2_SWITCHER.is_file():
        raise FileNotFoundError(f"Не найден v2 switcher: {V2_SWITCHER}")
    if not SERVICE_PATCHER.is_file():
        raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")

    source = BOT_FILE.read_text(encoding="utf-8")
    v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
    service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")

    source, v2_changes = v2.patch(source)
    source, service_changes = service.patch(source)
    compile(source, str(BOT_FILE), "exec")

    return source, [
        "cashier v2: " + ("; ".join(v2_changes) if v2_changes else "already active"),
        "service orders: " + (
            "; ".join(service_changes) if service_changes else "already integrated"
        ),
    ]


def live_service_preflight(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        present = tables(conn)
        required = {
            "payments",
            "service_orders",
            "service_order_steps",
            "service_order_payment_links",
            "remote_order_details",
            "remote_assets",
        }
        missing = sorted(required - present)
        if missing:
            raise RuntimeError(
                "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
            )

        payment_columns = columns(conn, "payments")
        print("Preflight:")
        print(
            "  payments.source_ref:",
            "present" if "source_ref" in payment_columns
            else "not present (compatible mode will be used)",
        )
        print(
            "  payments.apartment_id:",
            "present" if "apartment_id" in payment_columns
            else "not present (apartment_number mode will be used)",
        )

        order = conn.execute(
            """
            SELECT id, order_number, apartment_id, apartment_number,
                   service_item_code, service_name_snapshot,
                   order_status, payment_status, fulfillment_status
            FROM service_orders
            WHERE order_status NOT IN ('COMPLETED', 'CANCELLED')
            ORDER BY id ASC
            LIMIT 1
            """
        ).fetchone()
        if order:
            print(
                "  current open order:",
                f"{order['order_number']} | кв.{order['apartment_number']} | "
                f"{order['service_name_snapshot']} | {order['order_status']}"
            )
            if "apartment_id" in payment_columns:
                payment_where = "apartment_id = ?"
                apartment_value: Any = order["apartment_id"]
            else:
                payment_where = "CAST(apartment_number AS TEXT) = ?"
                apartment_value = str(order["apartment_number"])

            candidates = conn.execute(
                f"""
                SELECT COUNT(*)
                FROM payments
                WHERE {payment_where}
                  AND COALESCE(service_item_code, '') = COALESCE(?, '')
                  AND COALESCE(cashier_entry_status, 'CONFIRMED') = 'CONFIRMED'
                  AND COALESCE(amount, 0) > 0
                """,
                (apartment_value, order["service_item_code"]),
            ).fetchone()[0]
            print("  matching confirmed payments for this order:", int(candidates))
        else:
            print("  current open order: none")
    finally:
        conn.close()


def conflicting_guard_processes() -> list[str]:
    command = (
        "Get-CimInstance Win32_Process | "
        "Where-Object { ($_.Name -eq 'python.exe' -or $_.Name -eq 'pythonw.exe') "
        "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
        "ForEach-Object { 'PID=' + $_.ProcessId + ' | ' + $_.CommandLine }"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
            check=False,
        )
    except Exception:
        return []

    return [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]


def run_bot(source: str) -> None:
    os.chdir(BOTS_DIR)
    namespace = {
        "__name__": "__main__",
        "__file__": str(BOT_FILE),
        "__package__": None,
    }
    exec(compile(source, str(BOT_FILE), "exec"), namespace)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    parser.add_argument(
        "--no-permission-seed",
        action="store_true",
        help="Do not create sandbox-only service operator permissions.",
    )
    args = parser.parse_args()

    print("=" * 100)
    print("OSBB LIVE SERVICES SANDBOX")
    print("=" * 100)
    print("Database:", LIVE_SERVICES_DB)
    print("Mode:", "RUN TELEGRAM BOT" if args.run else "CHECK ONLY")

    if not LIVE_SERVICES_DB.is_file():
        raise FileNotFoundError(
            "Не найдена live-services sandbox-БД:\n"
            f"  {LIVE_SERVICES_DB}"
        )

    configure_sandbox(LIVE_SERVICES_DB)
    live_service_preflight(LIVE_SERVICES_DB)

    if args.no_permission_seed:
        print("Permission seed: skipped by --no-permission-seed")
    else:
        users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
        print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
        if backup:
            print("Sandbox backup before permission seed:", backup)
        print(
            "Permission seed:",
            f"{len(changes)} change(s)" if changes else "already prepared",
        )

    assert_workspace_is_compatible()
    purge_project_modules()
    source, bot_changes = patch_bot_source()

    print("Runtime changes:")
    print("  - service_orders workspace: compatibility verified")
    for item in bot_changes:
        print("  -", item)

    if not args.run:
        print()
        print("CHECK PASSED")
        print("No Telegram polling was started.")
        print("Bots\\parking_bot.py and config.py were not changed.")
        return 0

    conflicts = conflicting_guard_processes()
    if conflicts:
        print()
        print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
        for item in conflicts:
            print("  ", item)
        print("Stop them with Ctrl+C, then run this launcher again.")
        return 2

    print()
    print("Starting live services sandbox bot.")
    print("All order/payment/remote test changes go only to:")
    print(" ", LIVE_SERVICES_DB)
    print("Stop this bot with Ctrl+C.")
    print()
    run_bot(source)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nLive services sandbox bot stopped by Ctrl+C.")
        raise SystemExit(0)
    except Exception:
        print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
        traceback.print_exc()
        raise SystemExit(1)
